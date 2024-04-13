from celery import shared_task
import logging

logger = logging.getLogger(__name__)

from base.utils import MomoTransaction
from base.models import Payments
transaction = MomoTransaction()


@shared_task
def validate_pending_transactions():
    subs = Payments.objects.filter(sub_status="pending")
    logger.warning("fetching pending Paymentss")
    subs_to_update = []
    for sub in subs:
        if sub.reference_id:
            verify = transaction.verify_transaction(sub.reference_id)
            logger.warning(verify)
            if verify == "success":
                sub.sub_status = "completed"
                subs_to_update.append(sub)
            else:
                logger.warning(f"transaction {sub.reference_id} returned {verify}")

    if subs_to_update:
        Payments.objects.bulk_update(subs_to_update, ['sub_status'])

    return "Pending subscriptions updated"