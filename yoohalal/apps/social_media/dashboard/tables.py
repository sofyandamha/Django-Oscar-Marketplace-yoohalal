from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
LinkType = get_model('social_media', 'LinkType')


class LinkTypeTable(DashboardTable):
	check = TemplateColumn(
		template_name='dashboard/linktype/linktype_row_checkbox.html',
		verbose_name=' ', orderable=False)
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/linktype/linktype_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = LinkType
		template = 'dashboard/linktype/table.html'
		fields = ('name', 'url', 'is_visible', 'order_number')
		sequence = ('check', 'name', 'url', 'is_visible', 'order_number')
		order_by = 'order_number'