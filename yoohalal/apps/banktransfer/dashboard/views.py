from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, FormView

from oscar.core.loading import get_class, get_model

from django_tables2 import SingleTableView

TransactionTable = get_class('banktransfer.dashboard.tables', 'TransactionTable')
BankTransferSearchForm = get_class('banktransfer.dashboard.forms', 'BankTransferSearchForm')
BankTransferTransaction = get_model('banktransfer', 'BankTransferTransaction')


class TransactionListView(SingleTableView):
	model = BankTransferTransaction
	form_class = BankTransferSearchForm
	table_class = TransactionTable
	context_table_name = 'transactions'
	template_name = 'dashboard/banktransfer/transaction_list.html'
	
	def get_context_data(self, **kwargs):
		ctx = super(TransactionListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Transactions search results')
		return _('Transactions')

	def get_table(self, **kwargs):
		table = super(TransactionListView, self).get_table(**kwargs)
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


class TransactionDetailView(DetailView):
	model = BankTransferTransaction
	context_object_name = 'txn'
	template_name = 'dashboard/banktransfer/transaction_detail.html'