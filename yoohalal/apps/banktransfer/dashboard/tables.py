from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
BankTransferTransaction = get_model('banktransfer', 'BankTransferTransaction')


class TransactionTable(DashboardTable):
	order_number = LinkColumn('dashboard:order-detail', args=[A('order_number')])

	amount = TemplateColumn(
        verbose_name=_('Amount'),
        template_name='dashboard/banktransfer/banktransfer_row_amount.html')

	date_confirmed = TemplateColumn(
        verbose_name=_('Date Confirmed'),
        template_name='dashboard/banktransfer/banktransfer_row_date_confirmed.html',
        orderable=False)

	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/banktransfer/banktransfer_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = BankTransferTransaction
		fields = ('order_number', 'bank_account', 'amount',
				  'confirmed', 'date_confirmed')
		sequence = ('order_number', 'bank_account', 'amount',
					'confirmed', 'date_confirmed')
		order_by = '-date_created'