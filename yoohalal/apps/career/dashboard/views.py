from django.views.generic import (
	CreateView, DeleteView, ListView, UpdateView, FormView, DetailView)
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from oscar.apps.customer.utils import normalise_email

from apps.career.forms import CareerForm, DepartementForm
from apps.career.models import Applicant, Career, Departement
from apps.career.dashboard.tables import (
	DepartementTable, CareerTable, ApplicantTable)
from apps.career.dashboard.forms import (
	DepartementSearchForm, ApplicantSearchForm, CareerSearchForm)

from django_tables2 import SingleTableView


# ============
# CAREER
# ============


class CareerCreateView(CreateView):
	model = Career
	form_class = CareerForm
	template_name = 'dashboard/career/career_form.html'
	success_url = reverse_lazy('career-list')

	def get_success_url(self):
		messages.info(self.request, _("Career created successfully"))
		return super(CareerCreateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(CareerCreateView, self).get_context_data(**kwargs)
		ctx['title'] = _("Create new career")
		return ctx


class CareerUpdateView(UpdateView):
	model = Career
	form_class = CareerForm
	template_name = 'dashboard/career/career_form.html'
	success_url = reverse_lazy('career-list')

	def get_success_url(self):
		messages.info(self.request, _("Career updated successfully"))
		return super(CareerUpdateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(CareerUpdateView, self).get_context_data(**kwargs)
		ctx['career'] = self.object
		ctx['title'] = self.object.title
		return ctx


class CareerDeleteView(DeleteView):
	model = Career
	context_object_name = 'career'
	template_name = 'dashboard/career/career_delete.html'

	def get_success_url(self):
		messages.info(self.request, _("Career deleted"))
		return reverse('career-list')


class CareerListView(SingleTableView):
	model = Career
	table_class = CareerTable
	form_class = CareerSearchForm
	context_table_name = 'careers'
	template_name = 'dashboard/career/career_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(CareerListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Careers search results')
		return _('Careers')

	def get_table(self, **kwargs):
		table = super(CareerListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def get_queryset(self):
		queryset = self.model.objects.all()
		self.form = self.form_class(self.request.GET)
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['title']:
			queryset = queryset.filter(title__icontains=data['title'])
		return queryset


class CareerDetailView(DetailView):
	model = Career
	context_object_name = 'career'
	template_name = 'dashboard/career/career_detail.html'


# =============
# DEPARTEMENT
# =============


class DepartementCreateView(CreateView):
	model = Departement
	form_class = DepartementForm
	template_name = 'dashboard/departement/departement_form.html'
	success_url = reverse_lazy('departement-list')

	def get_success_url(self):
		messages.info(self.request, _("Departement created successfully"))
		return super(DepartementCreateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(DepartementCreateView, self).get_context_data(**kwargs)
		ctx['title'] = _("Create new departement")
		return ctx


class DepartementUpdateView(UpdateView):
	model = Departement
	form_class = DepartementForm
	template_name = 'dashboard/departement/departement_form.html'
	success_url = reverse_lazy('departement-list')

	def get_success_url(self):
		messages.info(self.request, _("Departement updated successfully"))
		return super(DepartementUpdateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(DepartementUpdateView, self).get_context_data(**kwargs)
		ctx['departement'] = self.object
		ctx['title'] = self.object.departement
		return ctx


class DepartementDeleteView(DeleteView):
	model = Departement
	context_object_name = 'departement'
	template_name = 'dashboard/departement/departement_delete.html'

	def get_success_url(self):
		messages.info(self.request, _("Departement deleted"))
		return reverse('departement-list')


class DepartementListView(SingleTableView):
	model = Departement
	table_class = DepartementTable
	form_class = DepartementSearchForm
	context_table_name = 'departements'
	template_name = 'dashboard/departement/departement_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(DepartementListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Departements search results')
		return _('Departements')

	def get_table(self, **kwargs):
		table = super(DepartementListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def get_queryset(self):
		queryset = self.model.objects.all()
		self.form = self.form_class(self.request.GET)
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['departement']:
			queryset = queryset.filter(departement__icontains=data['departement'])
		return queryset


class DepartementDetailView(DetailView):
	model = Departement
	context_object_name = 'departement'
	template_name = 'dashboard/departement/departement_detail.html'


# =============
# APPLICANT
# =============


class ApplicantListView(SingleTableView):
	model = Applicant
	table_class = ApplicantTable
	form_class = ApplicantSearchForm
	context_table_name = 'applicants'
	desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
	template_name = 'dashboard/applicant/applicant_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(ApplicantListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_table(self, **kwargs):
		table = super(ApplicantListView, self).get_table(**kwargs)
		table.caption = self.desc_template % self.desc_ctx
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def get_queryset(self):
		queryset = self.model.objects.all()
		self.form = self.form_class(self.request.GET)
		return self.apply_search(queryset)

	def apply_search(self, queryset):
		self.desc_ctx = {
			'main_filter': _('All applicants'),
			'email_filter': '',
			'name_filter': '',
		}
		if self.form.is_valid():
			return self.apply_search_filters(queryset, self.form.cleaned_data)
		else:
			return queryset

	def apply_search_filters(self, queryset, data):
		if data['email']:
			email = normalise_email(data['email'])
			queryset = queryset.filter(email__istartswith=email)
			self.desc_ctx['email_filter'] \
				= _(" with email matching '%s'") % email
		if data['name']:
			parts = data['name'].split()
			condition = Q()
			for part in parts:
				condition &= Q(name__icontains=part)
			queryset = queryset.filter(condition).distinct()
			self.desc_ctx['name_filter'] \
				= _(" with name matching '%s'") % data['name']
		return queryset


class ApplicantDetailView(DetailView):
	model = Applicant
	context_object_name = 'applicant'
	template_name = 'dashboard/applicant/applicant_detail.html'


class ApplicantDeleteView(DeleteView):
	model = Applicant
	context_object_name = 'applicant'
	template_name = 'dashboard/applicant/applicant_delete.html'

	def get_success_url(self):
		messages.info(self.request, _("Applicant deleted"))
		return reverse('applicant-list')