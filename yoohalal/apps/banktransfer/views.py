from django import http
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from oscar.apps.payment.models import SourceType, Source
from oscar.apps.checkout.views import PaymentDetailsView

from .forms import BankAccountForm
from . import gateway


class PaymentDetailsView(PaymentDetailsView):
	template_name = 'banktransfer/payment_details.html'
	template_name_preview = 'banktransfer/preview.html'

	def handle_payment_details_submission(self, request):
		bank_account_form = BankAccountForm(request.POST)
		if bank_account_form.is_valid():
			return self.render_preview(
				request, bank_account_form=bank_account_form)

		return self.render_payment_details(
			request, bank_account_form=bank_account_form)


	def handle_place_order_submission(self, request):
		bank_account_form = BankAccountForm(request.POST)
		if bank_account_form.is_valid():
			submission = self.build_submission(
				payment_kwargs={
					'bank_account': bank_account_form.cleaned_data['bank_account']
				})

			return self.submit(**submission)

		messages.error(request, _("Invalid submission"))
		return http.HttpResponseRedirect(
			reverse('checkout:payment-details'))


	def build_submission(self, **kwargs):
		submission = super(PaymentDetailsView, self).build_submission(**kwargs)
		submission['payment_kwargs']['shipping_address'] = submission['shipping_address']
		return submission


	def handle_payment(self, order_number, total, **kwargs):
		bank_account = kwargs['bank_account']
		reference = gateway.create_transaction(order_number,total,bank_account)
		source_type, is_created = SourceType.objects.get_or_create(name=_('Bank Transfer'))
		source = Source(source_type=source_type, currency=total.currency, amount_allocated=total.incl_tax, amount_debited=0)
		self.add_payment_source(source)
		self.add_payment_event('Issued', total.incl_tax, reference=reference)


	def get_context_data(self, **kwargs):
		ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
		ctx['bank_account_form'] = kwargs.get('bank_account_form', BankAccountForm())
		return ctx