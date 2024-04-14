import logging

logger = logging.getLogger(__name__)
import requests
from decouple import config
from post_office import mail


class Notify:
    def send_sms_or_email(self, medium, recipient, message=None, context=None):
        if medium == "sms":
            phone = recipient
            logger.warning(phone)
            apiKey = config("SMS_KEY")
            endPoint = "https://api.mnotify.com/api/sms/quick"
            data = {
                "recipient[]": [phone],
                "sender": "DBANKER",
                "message": message,
                "is_schedule": False,
                "schedule_date": "",
            }
            url = endPoint + "?key=" + apiKey
            response = requests.post(url, data)
            data = response.json()
            return
        # medium is email now
        template = context["template"]
        mail.send(
            recipient,
            config("DEFAULT_FROM_EMAIL"),
            template=template,
            context=context["context"],
            priority="now",
        )
