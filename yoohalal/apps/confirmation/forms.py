import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from oscar.forms import widgets
from oscar.core.loading import get_class, get_model
from oscar.apps.order.models import Order

from apps.customer.utils import Dispatcher


BankTransferTransaction = get_model('banktransfer', 'BankTransferTransaction')
ConfirmationPayment = get_model('confirmation', 'ConfirmationPayment')
CommunicationEventType = get_model('customer', 'CommunicationEventType')


class ConfirmationOrderForm(forms.Form):
	order_number = forms.CharField(max_length=128)

	def __init__(self, *args, **kwargs):
		super(ConfirmationOrderForm, self).__init__(*args, **kwargs)
		self.fields['order_number'].label = _('Order Number')

	def clean_order_number(self):
		order_number = self.cleaned_data.get("order_number")
		if not Order.objects.filter(number=order_number).exists():
			raise forms.ValidationError(
							_('Order number "%(order_number)s" is not found'),
							params={'order_number': order_number},
						)
		if ConfirmationPayment.objects.filter(order_number=order_number, status='accept').exists():
			raise forms.ValidationError(
							_('Confirmation with order number "%(order_number)s" has been accepted'),
							params={'order_number': order_number},
						)
		return order_number


class ConfirmationPostForm(forms.ModelForm):
	destination_bank = forms.ChoiceField(label=_('Destination Bank'), choices=())
	transfer_date = forms.DateTimeField(required=False, label=_('Transfer Date'),
										widget=widgets.DateTimePickerInput())
	note = forms.CharField(label=_('Note'), widget=forms.Textarea, required=False)

	def __init__(self, bank_account=None, *args, **kwargs):
		super(ConfirmationPostForm, self).__init__(*args, **kwargs)
		self.fields['destination_bank'].choices = self.initial_bank_choices()
		self.fields['proof_payment'].required = True
		self.fields['note'].widget.attrs['rows'] = 3
		for field in ['order_number', 'amount']:
			self.fields[field].widget.attrs['readonly'] = True

	def initial_bank_choices(self):
		bank_choices = []
		for bank in settings.BANK_ACCOUNT_LIST:
			bank_choices.append((bank['label'], bank['label']),)
		return bank_choices

	def send_email(self, site, recipient, number):
		code = 'CONFIRMATION'
		ctx = {'order_number' : number, 'site': site}
		try:
			event_type = CommunicationEventType.objects.get(code=code)
		except CommunicationEventType.DoesNotExist:
			messages = CommunicationEventType.objects.get_and_render(code, ctx)
		else:
			messages = event_type.get_messages(ctx)
		if messages and messages['body']:
			Dispatcher().dispatch_direct_messages(recipient, messages)

	def send_email_to_cs(self, site, sender, number):
		ctx = {'number':number, 'site':site, 'sender':sender}

		try:
			event_type = CommunicationEventType.objects.get(code='GET_NEW_CONFIRMATION')
		except CommunicationEventType.DoesNotExist:
			messages = CommunicationEventType.objects.get_and_render('GET_NEW_CONFIRMATION', ctx)
		else:
			messages = event_type.get_messages(ctx)

		if messages and messages['body']:
			Dispatcher().send_random_email_messages(messages, sender)

	def clean_order_number(self):
		order_number = self.cleaned_data.get("order_number")
		if not Order.objects.exclude(pk=self.instance.pk).filter(number=order_number).exists():
			raise forms.ValidationError(
							_('Order number "%(order_number)s" is not found'),
							params={'order_number': order_number},
						)
		if ConfirmationPayment.objects.filter(order_number=order_number, status='accept').exists():
			raise forms.ValidationError(
							_('Confirmation with order number "%(order_number)s" has been accepted'),
							params={'order_number': order_number},
						)
		return order_number

	def clean_proof_payment(self):
		proof_payment = self.cleaned_data['proof_payment']
		if proof_payment._size > settings.MAX_UPLOAD_SIZE:
			raise forms.ValidationError(
							_('Please keep filesize under "%(max_size)s". Current filesize "%(current_size)s"'),
							params={
								'max_size': filesizeformat(settings.MAX_UPLOAD_SIZE),
								'current_size': filesizeformat(proof_payment._size)},
							)
		return proof_payment

	class Meta:
		model = ConfirmationPayment
		fields = [
			'account_owner_name','transfer_date', 'destination_bank',
			'amount', 'order_number',  'customer_email',
			'customer_phone', 'note', 'proof_payment'
		]