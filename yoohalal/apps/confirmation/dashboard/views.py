from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, RedirectView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site

from django_tables2 import SingleTableView

from oscar.core.loading import get_class, get_model

ConfirmationTable = get_class('confirmation.dashboard.tables', 'ConfirmationTable')
ConfirmationSearchForm = get_class('confirmation.dashboard.forms', 'ConfirmationSearchForm')
CommunicationEventType = get_model('customer', 'CommunicationEventType')
BankTransferTransaction = get_model('banktransfer', 'BankTransferTransaction')
ConfirmationPayment = get_model('confirmation', 'ConfirmationPayment')
Dispatcher = get_class('customer.utils', 'Dispatcher')


class ConfirmationListView(SingleTableView):
	model = ConfirmationPayment
	form_class = ConfirmationSearchForm
	table_class = ConfirmationTable
	context_table_name = 'data'
	template_name = 'dashboard/confirmation/data_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(ConfirmationListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Confirmation search results')
		return _('Confirmation')

	def get_table(self, **kwargs):
		table = super(ConfirmationListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def get_queryset(self):
		queryset = self.model.objects.all().order_by('id')

		self.form = self.form_class(self.request.GET)
		if not self.form.is_valid():
			return queryset

		data = self.form.cleaned_data

		if data['order_number']:
			queryset = queryset.filter(order_number__icontains=data['order_number'])

		return queryset


class ConfirmationDetailView(DetailView):
	model = ConfirmationPayment
	context_object_name = 'txn'
	template_name = 'dashboard/confirmation/data_detail.html'


class ConfirmationChangeStatusView(RedirectView):
	url = reverse_lazy('confirmation-method-list')
	permanent = False
	accept_code = "ACCEPT_CONFIRMATION"
	reject_code = "REJECT_CONFIRMATION"

	def get(self, request, pk=None, action=None, *args, **kwargs):
		confirmation = get_object_or_404(ConfirmationPayment, pk=pk)
		obj = BankTransferTransaction.objects.get(order_number=confirmation.order_number)
		
		if action == 'accept':
			setattr(confirmation, 'status', 'accept')
			if obj:
				setattr(obj, 'confirmed', True)
				setattr(obj, 'date_confirmed', confirmation.date_created)
				obj.save()
				self.send_email_confirmation(request,
					self.accept_code, confirmation.customer_email)
		elif action == 'reject':
			setattr(confirmation, 'status', 'reject')
			if obj:
				setattr(obj, 'confirmed', False)
				setattr(obj, 'date_confirmed', confirmation.date_created)
				obj.save()
				self.send_email_confirmation(request,
					self.reject_code, confirmation.customer_email)
		else:
			setattr(confirmation, 'status', 'pending')
		confirmation.save()

		return super(ConfirmationChangeStatusView, self).get(
			request, *args, **kwargs)

	def send_email_confirmation(self, request=None, code=None, email=None):
		site = get_current_site(request)
		ctx = {
			'email': email,
			'site': site}
		messages = CommunicationEventType.objects.get_and_render(
			code=code, context=ctx)
		if messages and messages['body']:
			Dispatcher().dispatch_direct_messages(email, messages)