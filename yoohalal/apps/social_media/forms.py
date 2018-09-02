from django import forms

from .models import LinkType


class LinkTypeForm(forms.ModelForm):

	class Meta:
		model = LinkType
		fields = ('name', 'url', 'is_visible', 'order_number')