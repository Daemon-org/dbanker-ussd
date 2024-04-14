import json
from django.shortcuts import render
import arrow as arrow
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from base.templates import registered_users, non_users
from base.models import UssdLog,Transaction, UssdSession, Profile
from base.utils import MomoTransaction, fix_email
from base.notify import Notify
from django.core.cache import cache
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)
# Create your views here.

trans = MomoTransaction()
notify = Notify()


def package(body, template, status="1"):
    data = {
        "msg_type": status,
        "ussd_body": template,
        "session_id": body["session_id"],
        "msisdn": body["msisdn"],
        "nw_code": body["nw_code"],
        "service_code": body["service_code"],
    }
    return data


@csrf_exempt
def index(request):
    now = arrow.now().datetime
    try:
        body = json.loads(request.body)
        session_id = body["session_id"]
        phone_number = body["msisdn"]
        response = body["ussd_body"]
        session_check = UssdLog.objects.filter(session_id=session_id)

        if session_check.exists():
            logger.warning("session exists")
            logger.warning(body)
            log = session_check[0]
            stage = session_check[0].stage

            if stage == "n1":
                logger.warning("registering new user")
                if response == "1":
                    template = non_users["n2"]
                    data = package(body, template["body"], status=template["status"])
                    log.stage = "n2"
                    log.save(update_fields=["stage"])
                    return JsonResponse(data)

                if response == "2":
                    logger.warning("about us")
                    template = non_users["n5"]
                    data = package(body, template["body"], status=template["status"])
                    log.stage = "n5"
                    log.save(update_fields=["stage"])
                    return JsonResponse(data)

                if response == "3":
                    logger.warning("contact us")
                    template = non_users["n6"]
                    data = package(body, template["body"], status=template["status"])
                    log.stage = "n6"
                    log.save(update_fields=["stage"])
                    return JsonResponse(data)

            if stage == "n5":
                template = non_users["n5"]["body"]
                inp = response.strip()

                if inp == "1":
                    template = non_users["n1"]
                    log.stage = "n1"
                    log.save(update_fields=["stage"])
                    data = package(body, template["body"], status=template["status"])
                    return JsonResponse(data)

            if stage == "n6":
                template = non_users["n6"]["body"]
                inp = response.strip()

                if inp == "1":
                    template = non_users["n1"]
                    log.stage = "n1"
                    log.save(update_fields=["stage"])
                    data = package(body, template["body"], status=template["status"])
                    return JsonResponse(data)

            if stage == "n2":
                logger.warning("enter email")
                template = non_users["n2"]
                email = response.strip().replace(";", "@")  # Replace ';' with '@'
                email = fix_email(email)
                session_cache = json.loads(cache.get(session_id, "{}"))
                session_cache["email"] = email
                cache.set(session_id, json.dumps(session_cache))
                template = non_users["n3"]
                log.stage = "n3"
                log.save(update_fields=["stage"])
                data = package(body, template["body"], status=template["status"])
                return JsonResponse(data)

            if stage == "n3":
                logger.warning("enter pincode")
                template = non_users["n3"]["body"]
                code = response.strip()

                if len(code) == 4 and code.isdigit():
                    session_cache = json.loads(cache.get(session_id, "{}"))
                    session_cache["pincode"] = code
                    cache.set(session_id, json.dumps(session_cache))
                    template = non_users["n4"]
                    log.stage = "n4"

                else:
                    error_template = non_users["n3"]
                    data = package(
                        body, error_template["error"], status=template["status"]
                    )
                    return JsonResponse(data, safe=False)

            if stage == "n4":
                logger.warning("confirm pincode")
                template = non_users["n4"]["body"]
                usdd = response.strip()
                if len(usdd) == 4 and usdd.isdigit():
                    ussd_pin = make_password(usdd)
                    try:
                        session_cache = json.loads(cache.get(session_id, "{}"))
                        email = session_cache.get("email", "")
                        full_name = session_cache.get("name", "")
                        confirm_pin = session_cache.get("pincode", "")

                        if confirm_pin != usdd:
                            error_template = non_users["n3"]
                            data = package(
                                body, error_template["error"], status=template["status"]
                            )
                            return JsonResponse(data, safe=False)

                        user = Profile.objects.create(
                            email=email,
                            phone_number=phone_number,
                            full_name=full_name,
                            pincode=ussd_pin,
                        )
                        logger.info(user)
                        data = {
                            "session": session_id,
                            "phone_number": phone_number,
                            "email": email,
                            "pincode": ussd_pin,
                        }
                        cache.set(session_id, json.dumps(data))
                        template = registered_users["r1"]
                        log.stage = template["next"]
                        body["email"] = email
                        body["phone_number"] = phone_number
                        cache.set(session_id, json.dumps(body))
                        log.save(update_fields=["stage"])
                        data = package(
                            body, template["body"], status=template["status"]
                        )
                        return JsonResponse(data)
                    except Exception as e:
                        error_template = non_users["n3"]
                        data = package(
                            body, error_template["error"], status=template["status"]
                        )
                        return JsonResponse(data, safe=False)

                if stage == "r1":
                    logger.warning("returning user")
                    template = registered_users["r1"]["body"]

                    if response == "1":
                        logger.warning("send cash")
                        template = registered_users["s2"]
                        data = package(
                            body, template=template["body"], status=template["status"]
                        )
                        log.stage = "s2"
                        log.save(update_fields=["stage"])
                        return JsonResponse(data)

                    if response == "2":
                        logger.warning("deposit cash")
                        template = registered_users["d2"]
                        data = package(
                            body, template=template["body"], status=template["status"]
                        )
                        log.stage = "d2"
                        log.save(update_fields=["stage"])
                        return JsonResponse(data)

                    if response == "3":
                        logger.warning("withdraw cash")
                        template = registered_users["w2"]
                        data = package(
                            body, template=template["body"], status=template["status"]
                        )
                        log.stage = "w2"
                        log.save(update_fields=["stage"])
                        return JsonResponse(data)

                    if response == "4":
                        logger.warning("transfer statements")
                        template = registered_users["x1"]
                        data = package(
                            body, template=template["body"], status=template["status"]
                        )
                        log.stage = "x1"
                        log.save(update_fields=["stage"])
                        return JsonResponse(data)

                if stage == "s2":
                    logger.warning("enter receipient number")
                    template = registered_users["s2"]
                    receiver = response.strip()
                    session_cache = json.loads(cache.get(session_id, "{}"))
                    session_cache["receiver"] = receiver
                    cache.set(session_id, json.dumps(session_cache))
                    data = package(
                        body, template=template["body"], status=template["status"]
                    )
                    log.stage = "s3"
                    log.save(update_fields=["stage"])
                    return JsonResponse(data)

                if stage == "s3":
                    logger.warning("enter amount")
                    template = registered_users["s3"]
                    amount = response.strip()
                    session_cache = json.loads(cache.get(session_id, "{}"))
                    session_cache["amount"] = amount
                    cache.set(session_id, json.dumps(session_cache))
                    data = package(
                        body, template=template["body"], status=template["status"]
                    )
                    log.stage = "s4"
                    log.save(update_fields=["stage"])
                    return JsonResponse(data)

                if stage == "s4":
                    template = registered_users["s4"]
                    session_cache = json.loads(cache.get(session_id, "{}"))
                    receiver = session_cache.get("receiver", "")
                    amount = Decimal(session_cache.get("amount", ""))
                    s_user = Profile.objects.get(phone_number=phone_number)
                    r_user = Profile.objects.get(phone_number=receiver)
                    if r_user:
                        template = template["body"]
                        template.format(
                            r_user.full_name,
                            amount,
                        )

                    else:
                        error_template = registered_users["s4"]
                        data = package(
                            body, error_template["error"], status=template["status"]
                        )
                        return JsonResponse(data, safe=False)
                     
                    total_amount = trans.add_charges(amount)
                   # TODO: pin code input before send

                    if s_user.balance >= total_amount:
                        s_user.balance -= total_amount
                        r_user.balance += amount
                        s_user.save(update_fields=["balance"])
                        r_user.save(update_fields=["balance"])
                        Transaction.objects.create(
                            profile = s_user,
                            amount = amount,
                            transaction_type = "transfer",
                            receipient_number = r_user.phone_number
                        )


                    else:
                        error_template = registered_users["s4"]
                        data = package(
                            body, error_template["error2"], status=template["status"]
                        )
                        return JsonResponse(data, safe=False)
                
                    return JsonResponse(data)
                
                if stage == "d2":
                    pass




        else:
            logger.info("-- new ussd session --")
            UssdSession(body=body, date_created=now, type=body["msg_type"]).save()
            log = UssdLog.objects.create(
                session_id=session_id,
                phone="+{0}".format(body["msisdn"]),
                message_type=body["msg_type"],
            )
            user_checker = Profile.objects.filter(
                ussd_number=phone_number, isBanned=False
            )

            if user_checker.exists():
                logger.warning("Returning user")
                template = registered_users["r1"]
                log.stage = "r1"
                log.save()
                data = package(body, template["body"])
                return JsonResponse(data)
            else:
                template = non_users["n1"]
                log.stage = "n1"
                log.save(update_fields=["stage"])
                data = package(body, template["body"])
                return JsonResponse(data)

    except Exception as e:
        logger.warning(str(e))
        return JsonResponse({})
