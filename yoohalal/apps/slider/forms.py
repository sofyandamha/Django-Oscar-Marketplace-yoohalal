from django import forms
from .models import SliderImage

class SliderForm(forms.ModelForm):

	class Meta:
		model = SliderImage
		fields = ('image', 'is_visible', 'slider_number', 'html_caption')