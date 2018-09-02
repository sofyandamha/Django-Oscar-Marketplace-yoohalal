from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Category = get_model('blog', 'Category')
PostEntry = get_model('blog', 'PostEntry')


class CategoryTable(DashboardTable):
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/category/category_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = Category
		fields = ('category',)
		sequence = ('category',)
		order_by = 'category'


class PostTable(DashboardTable):
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/post/post_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = PostEntry
		fields = ('title', 'author', 'category',
				  'created', 'published')
		sequence = ('title', 'author', 'category',
					'created', 'published')
		order_by = '-created'