import json
import urllib

from django import forms
from django.conf import settings
from django.forms.utils import ErrorList
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site

from oscar.core.loading import get_class, get_model
from oscar.apps.order.models import Order


BankTransferTransaction = get_model('banktransfer', 'BankTransferTransaction')
ConfirmationPayment = get_model('confirmation', 'ConfirmationPayment')
ConfirmationPostForm = get_class('confirmation.forms', 'ConfirmationPostForm')
ConfirmationOrderForm = get_class('confirmation.forms', 'ConfirmationOrderForm')


class ConfirmationOrderView(FormView):
	form_class = ConfirmationOrderForm
	template_name = 'confirmation/confirmation_order_form.html'

	def form_valid(self, form):
		return HttpResponseRedirect(self.get_success_url(order_number = form.cleaned_data['order_number']))

	def get_success_url(self, **kwargs):
		return reverse_lazy('confirmation:confirmation-payment', kwargs = {'order_number': kwargs['order_number']})


class ConfirmationPaymentView(FormView):
	form_class = ConfirmationPostForm
	template_name = 'confirmation/confirmation_form.html'

	def get_form_kwargs(self):
		kwargs = super(ConfirmationPaymentView, self).get_form_kwargs()
		if 'order_number' in self.kwargs:
			data = BankTransferTransaction.objects.get(order_number=self.kwargs['order_number'])
			if data:
				kwargs['instance'] = ConfirmationPayment(
										order_number=data.order_number,
										amount=data.amount,
										destination_bank= data.bank_account
									 )
		return kwargs

	def form_valid(self, form):
		recaptcha_response = self.request.POST.get('g-recaptcha-response')
		url = 'https://www.google.com/recaptcha/api/siteverify'
		values = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
		}

		data = urllib.parse.urlencode(values).encode("utf-8")
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req, data=data)
		result = json.load(response)

		if result['success']:
			obj = form.save()
			form.send_email(get_current_site(self.request), obj.customer_email, obj.order_number)
			form.send_email_to_cs(get_current_site(self.request), obj.customer_email, obj.order_number)
			return HttpResponseRedirect(self.get_success_url(order_number = obj.order_number))
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'Invalid reCAPTCHA. Please try again.'
				])
			return self.form_invalid(form)

	def get_success_url(self, **kwargs):
		return reverse_lazy('confirmation:confirmation-success', kwargs = {'order_number': kwargs['order_number']})


class ConfirmationSuccessView(DetailView):
	template_name = 'confirmation/success.html'
	context_object_name = 'order'
	model = Order

	def get(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
		except Http404:
			return reverse_lazy('confirmation:payment-page', kwargs = {'order_number': self.kwargs['order_number']})
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_object(self):
		obj = get_object_or_404(Order,number=self.kwargs['order_number'])
		return obj