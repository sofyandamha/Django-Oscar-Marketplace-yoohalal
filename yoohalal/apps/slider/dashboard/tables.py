from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
SliderImage = get_model('slider', 'SliderImage')


class SliderImageTable(DashboardTable):
	check = TemplateColumn(
		template_name='dashboard/slider/slider_row_checkbox.html',
		verbose_name=' ', orderable=False)
	image = TemplateColumn(
        verbose_name=_('Image'),
        template_name='dashboard/slider/slider_row_image.html',
        orderable=False)
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/slider/slider_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = SliderImage
		template = 'dashboard/slider/table.html'
		fields = ('image', 'is_visible', 'slider_number')
		sequence = ('check', 'image', 'is_visible', 'slider_number')
		order_by = 'id'