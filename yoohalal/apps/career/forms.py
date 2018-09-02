from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.template.defaultfilters import filesizeformat

from oscar.forms import widgets
from oscar.core.loading import get_model
from oscar.views.generic import PhoneNumberMixin

from phonenumber_field.phonenumber import PhoneNumber


Applicant = get_model('career', 'Applicant')
Career = get_model('career', 'Career')
Departement = get_model('career', 'Departement')
Country = get_model('address', 'Country')


class CareerForm(forms.ModelForm):
	body = forms.CharField(required=False, label=_('Body'),
						widget=widgets.WYSIWYGTextArea())
	date_published = forms.DateTimeField(required=False,
						label=_('Date Published'),
						widget=widgets.DateTimePickerInput())

	class Meta:
		model = Career
		fields = ('title', 'date_published', 'departement', 'body', 'published')

	def clean_title(self):
		if not self.instance.id:
			if Career.objects.filter(slug=slugify(self.cleaned_data['title'])).exists():
				raise forms.ValidationError('Career with this title already exists.')
		else:
			if Career.objects.filter(title=self.cleaned_data['title']).exclude(id=self.instance.id):
				raise forms.ValidationError('Career with this title already exists.')
		return self.cleaned_data['title']


class ApplicantForm(PhoneNumberMixin, forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ApplicantForm, self).__init__(*args, **kwargs)
		self.adjust_country_field()
		self.fields.pop('career', None)

	def adjust_country_field(self):
		countries = Country._default_manager.filter(
			is_shipping_country=True)

		# No need to show country dropdown if there is only one option
		if len(countries) == 1:
			self.fields.pop('country', None)
			self.instance.country = countries[0]
		else:
			self.fields['country'].queryset = countries
			self.fields['country'].empty_label = None
	
	def clean_email(self):
		email = self.cleaned_data['email']
		if Applicant.objects.filter(email=email).exists():
			raise forms.ValidationError(_("Email already exists"))
		return email

	def clean_document(self):
		document = self.cleaned_data['document']
		if document._size > settings.MAX_UPLOAD_SIZE:
			raise forms.ValidationError(
							_('Please keep filesize under "%(max_size)s". Current filesize "%(current_size)s"'),
							params={
								'max_size': filesizeformat(settings.MAX_UPLOAD_SIZE),
								'current_size': filesizeformat(document._size)},
							)
		return document

	class Meta:
		model = Applicant
		fields = ('name', 'email', 'phone_number', 'career', 'document', 'country')


class DepartementForm(forms.ModelForm):

	def clean_departement(self):
		if not self.instance.id:
			if Departement.objects.filter(slug=slugify(self.cleaned_data['departement'])).exists():
				raise forms.ValidationError('Departement with this Name already exists.')
		else:
			if Departement.objects.filter(departement__icontains=self.cleaned_data['departement']).exclude(id=self.instance.id):
				raise forms.ValidationError('Departement with this Name already exists.')
		return self.cleaned_data['departement']

	class Meta:
		model = Departement
		fields = ('departement',)
