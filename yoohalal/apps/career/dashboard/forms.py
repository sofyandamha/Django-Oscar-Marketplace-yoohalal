from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy


class ApplicantSearchForm(forms.Form):
    email = forms.CharField(required=False, label=_("Email"))
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"Applicant's name", u"Name"))


class DepartementSearchForm(forms.Form):
	departement = forms.CharField(required=False, label=_("Departement"))


class CareerSearchForm(forms.Form):
	title = forms.CharField(required=False, label=_("Title"))