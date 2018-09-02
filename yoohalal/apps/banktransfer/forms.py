from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from oscar.forms import widgets

class BankAccountForm(forms.Form):

	bank_choices = []
	for bank in settings.BANK_ACCOUNT_LIST:
		bank_choices.append((bank['label'], bank['label']),)

	bank_account = forms.ChoiceField(widget=forms.RadioSelect, choices=bank_choices, required=True)