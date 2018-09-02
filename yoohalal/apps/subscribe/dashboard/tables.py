from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
SubscribeBase = get_model('subscribe', 'SubscribeBase')


class SubscribeTable(DashboardTable):
	check = TemplateColumn(
		template_name='dashboard/subscribe/subscribe_row_checkbox.html',
		verbose_name=' ', orderable=False)
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/subscribe/subscribe_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = SubscribeBase
		template = 'dashboard/subscribe/table.html'
		fields = ('email', 'is_active', 'date_created')
		sequence = ('check', 'email', 'is_active', 'date_created')
		order_by = '-date_created'