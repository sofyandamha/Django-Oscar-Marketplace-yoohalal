from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from oscar.forms import widgets

from .models import PostEntry, Category


class PostForm(forms.ModelForm):
	post_body = forms.CharField(required=False,
		label=_('Body'),
		widget=widgets.WYSIWYGTextArea())
	created = forms.DateTimeField(required=False,
		label=_('Date Published'),
		widget=widgets.DateTimePickerInput())

	class Meta:
		model = PostEntry
		fields = ('title', 'author', 'created', 'category', 'post_body', 'image', 'published')

	def clean_name(self):
		if not self.instance.id:
			if PostEntry.objects.filter(slug=slugify(self.cleaned_data['title'])).exists():
				raise forms.ValidationError('Blog with this title already exists.')
		else:
			if PostEntry.objects.filter(title=self.cleaned_data['title']).exclude(id=self.instance.id):
				raise forms.ValidationError('Blog with this title already exists.')

		return self.cleaned_data['category']


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('category',)

	def clean_name(self):
		if not self.instance.id:
			if Category.objects.filter(slug=slugify(self.cleaned_data['category'])).exists():
				raise forms.ValidationError('Category with this Name already exists.')
		else:
			if Category.objects.filter(category__icontains=self.cleaned_data['category']).exclude(id=self.instance.id):
				raise forms.ValidationError('Category with this Name already exists.')

		return self.cleaned_data['category']