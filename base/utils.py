from decimal import Decimal
import json
from decouple import config
import requests
import logging
from base.models import Profile,Transaction,Statements
import arrow
from base.notify import Notify
logger = logging.getLogger(__name__)

notify = Notify()


def fix_email(email):
    return email.replace("¡", "@")


class MomoTransaction:

    def check_network(self, phone_number):

        if len(phone_number) != 10:
            return "Invalid phone number"

        if phone_number[:3] in ["020", "050"]:
            network = "VOD"
        elif phone_number[:3] in ["027", "057", "026", "056"]:
            network = "ATL"
        elif phone_number[:3] in ["059", "024", "054"]:
            network = "MTN"

        return network
    
    def add_charges(self, amount):
        if amount <= Decimal(100):
            total = amount * Decimal('0.005')  # 0.5%
        elif amount <= Decimal(1000):
            total = amount * Decimal('0.01')  # 1%
        else:
            total = amount * Decimal('0.015')  # 1.5%
        return total + amount


    def send_mobile_money_prompt(self, amount, email, phone_number):
        endpoint = "https://api.paystack.co/charge"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        network = self.check_network(phone_number)
        logger.warning(network)
        # Prepare request payload
        payload = {
            "amount": int(amount) * 100,
            "email": email,
            "currency": "GHS",
            "mobile_money": {"phone": phone_number, "provider": network},
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def verify_transaction(self, reference):
        endpoint = f"https://api.paystack.co/transaction/verify/{reference}"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(endpoint, headers=headers)
        ret = response.json()

        return ret["data"]["status"]

    # all first transactions require otp verifications

    def verify_momo_otp(self, otp, reference):
        endpoint = f"https://api.paystack.co/charge/submit_otp"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        params = {"otp": otp, "reference": reference}

        params_json = json.dumps(params)

        response = requests.post(endpoint, data=params_json, headers=headers)

        res = response.json()
        return res["data"]["status"]

    """
    in order for this to work a reference should be created for the 
    particular user before sending the money
    """

    def create_mobile_money_recipient(self, name, account_number):
        endpoint = "https://api.paystack.co/transferrecipient"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        bank_code = self.check_network(account_number)

        logger.warning(bank_code)

        # Prepare request payload
        payload = {
            "type": "mobile_money",
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": "GHS",
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        print(f"momoreceipient :{response.json()}")
        return response.json()

    def transfer_funds(self, amount, phone_number, name):
        endpoint = "https://api.paystack.co/transfer"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        recipient_code = self.create_mobile_money_recipient(self, name, phone_number)
        # Prepare request payload
        payload = {
            "source": "balance",
            "amount": amount,
            "reference": config("PAYSTACK_REFERENCE"),
            "recipient": recipient_code["data"]["recipient_code"],
            "reason": "transfer",
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
    
    def withdraw_funds(self,amount,phone):
        user = Profile.objects.get(phone_number=phone)
        if user:
            trans = self.transfer_funds(amount,user.phone_number,user.full_name)

            if trans["data"]["status"] == 'success':
                Transaction.objects.create(
                    amount=amount,
                    profile=user,
                    receipient_number=user.phone_number,
                    transaction_type="withdraw",
                    status="completed",
                )
            else:
                return trans["data"]["status"]
            
        else:
            return "failed"
        
    def generate_trasaction_statements(self,phone):
        now = arrow.now()
        user = Profile.objects.get(phone_number=phone)
        transactions = Transaction.objects.filter(profile=user,created_at__year=now.year,created_at__month=now.month).order_by('-created_at')
        statements = []

        for transaction in transactions:
            statements.append({
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "status": transaction.status,
                "created_at": transaction.created_at
            })
        
        states = Statements.objects.bulk_create([Statements(**statement) for statement in statements])
        if states:
           notify.send_sms_or_email("sms",user.phone_number, states)
           return "success"
        
        else:
            return "failed"


    
       

        

