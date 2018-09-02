from django import forms
from django.utils.translation import ugettext_lazy as _


class CategorySearchForm(forms.Form):
	category = forms.CharField(required=False, label=_("Category"))


class PostSearchForm(forms.Form):
	title = forms.CharField(required=False, label=_("Title"))