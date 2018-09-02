from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
ConfirmationPayment = get_model('confirmation', 'ConfirmationPayment')


class ConfirmationTable(DashboardTable):
	order_number = LinkColumn('dashboard:order-detail', args=[A('order_number')])
	
	filename = TemplateColumn(
        verbose_name=_('Proof Of Payment'),
        template_name='dashboard/confirmation/confirmation_row_proof_payment.html',
        orderable=False)

	amount = TemplateColumn(
        verbose_name=_('Amount'),
        template_name='dashboard/confirmation/confirmation_row_amount.html')

	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/confirmation/confirmation_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = ConfirmationPayment
		fields = ('order_number', 'transfer_date', 'destination_bank',
				  'amount', 'status')
		sequence = ('order_number', 'transfer_date', 'destination_bank',
					'amount', 'filename', 'status', 'actions')
		order_by = '-date_created'