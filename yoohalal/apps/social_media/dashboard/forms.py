from django import forms
from django.utils.translation import ugettext_lazy as _


class LinkTypeSearchForm(forms.Form):
	name = forms.CharField(required=False, label=_("Name"))