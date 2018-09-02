from django import forms
from django.utils.translation import ugettext_lazy as _

class BankTransferSearchForm(forms.Form):
	order_number = forms.CharField(required=False, label=_("Order Number"))