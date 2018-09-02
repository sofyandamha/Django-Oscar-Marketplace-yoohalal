from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Departement = get_model('career', 'Departement')
Career = get_model('career', 'Career')


class ApplicantTable(DashboardTable):
	filename = TemplateColumn(
        verbose_name=_('Document'),
        template_name='dashboard/applicant/applicant_row_document.html',
        orderable=False)

	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/applicant/applicant_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = Career
		fields = ('name', 'email', 'phone_number', 'career',
			'date_created')
		sequence = ('name', 'email', 'phone_number', 'career',
			'filename', 'date_created')
		order_by = '-date_created'


class DepartementTable(DashboardTable):
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/departement/departement_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = Departement
		fields = ('departement',)
		sequence = ('departement',)
		order_by = 'departement'


class CareerTable(DashboardTable):
	actions = TemplateColumn(
		verbose_name=_('Actions'),
		template_name='dashboard/career/career_row_actions.html',
		orderable=False)

	icon = "sitemap"

	class Meta(DashboardTable.Meta):
		model = Career
		fields = ('title', 'departement', 'date_published', 'published')
		sequence = ('title', 'departement', 'date_published', 'published')
		order_by = '-date_published'