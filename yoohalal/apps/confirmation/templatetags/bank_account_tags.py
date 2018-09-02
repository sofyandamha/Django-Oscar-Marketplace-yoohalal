from django import template
from django.conf import settings
from apps.banktransfer.models import BankTransferTransaction

register = template.Library()

@register.assignment_tag
def bank_account_list():
    return settings.BANK_ACCOUNT_LIST

@register.assignment_tag
def get_bank_account_by_order(order_number):
	data = BankTransferTransaction.objects.filter(order_number=order_number)

	my_item = None

	if len(data) == 1:
		obj = data[0]

		for item in settings.BANK_ACCOUNT_LIST:
			if item['label'] == obj.bank_account:
				my_item = item
				break
	
	return my_item