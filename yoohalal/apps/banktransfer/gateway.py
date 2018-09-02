from django.db import transaction
from . import models


@transaction.atomic
def create_transaction(order_number, total, bank_account, *args, **kwargs):
    txn = models.BankTransferTransaction.objects.get_or_create(
        order_number=order_number,
        amount=total.incl_tax,
        currency=total.currency,
        bank_account=bank_account
    )
    return txn[0].reference