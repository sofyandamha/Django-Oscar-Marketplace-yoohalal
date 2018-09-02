from django import forms
from django.utils.translation import ugettext_lazy as _


class SliderSearchForm(forms.Form):

	YES_NO = (
		('','----'),
		(True, _("Yes")),
		(False, _("No")),
	)

	slider_number = forms.IntegerField(required=False,
		label=_("Slider Number"))
	is_visible = forms.ChoiceField(label=_("Is Visible"),
		initial='',required=False, choices=YES_NO)