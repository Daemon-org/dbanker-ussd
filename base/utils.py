from decimal import Decimal
import json
from decouple import config
import requests
import logging

logger = logging.getLogger(__name__)


class MomoTransaction:

    def check_network(self,phone_number):

        if len(phone_number) != 10:
            return "Invalid phone number"

        if phone_number[:3] in ["020", "050"]:
            network = "VOD"
        elif phone_number[:3] in ["027", "057", "026", "056"]:
            network = "ATL"
        elif phone_number[:3] in ["059", "024", "054"]:
            network = "MTN"

        return network




    def send_mobile_money_prompt(self,amount, email, phone_number):
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


    def verify_transaction(self,reference):
        endpoint = f"https://api.paystack.co/transaction/verify/{reference}"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(endpoint,headers=headers)
        ret = response.json()
        
        return ret["data"]["status"]


    # all first transactions require otp verifications

    def verify_momo_otp(self,otp,reference):
        endpoint = f"https://api.paystack.co/charge/submit_otp"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        params = {
        "otp":otp,
        "reference":reference 
        }

        params_json = json.dumps(params)

        response = requests.post(endpoint,data=params_json,headers=headers)

        res = response.json()
        return res["data"]["status"]



    """
    in order for this to work a reference should be created for the 
    particular user before sending the money
    """


    def create_mobile_money_recipient(self,name, account_number):
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


    def transfer_funds(self,amount, phone_number, name):
        endpoint = "https://api.paystack.co/transfer"
        secret_key = config("PAYSTACK_KEY")
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        recipient_code = self.create_mobile_money_recipient(self,name, phone_number)
        # Prepare request payload
        payload = {
            "source": "balance",
            "amount": amount,
            "reference": config("PAYSTACK_REFERENCE"),
            "recipient": recipient_code["data"]["recipient_code"],
            "reason": "Money Zone withdrawal",
        }

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()



        