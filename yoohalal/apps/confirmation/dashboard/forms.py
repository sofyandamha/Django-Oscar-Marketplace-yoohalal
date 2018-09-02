from django import forms
from django.utils.translation import ugettext_lazy as _

class ConfirmationSearchForm(forms.Form):
	order_number = forms.CharField(required=False, label=_("Order Number"))