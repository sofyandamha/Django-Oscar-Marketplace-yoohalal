from django.views.generic import (
	CreateView, DeleteView, ListView, UpdateView, DetailView)
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormMixin

from oscar.views.generic import BulkEditMixin
from oscar.core.loading import get_class, get_model

from django_tables2 import SingleTableView

from .tables import LinkTypeTable
from .forms import LinkTypeSearchForm

LinkType = get_model('social_media', 'LinkType')
LinkTypeForm = get_class('social_media.forms', 'LinkTypeForm')


class LinkTypeListView(BulkEditMixin, FormMixin, SingleTableView):
	model = LinkType
	table_pagination = True
	table_class = LinkTypeTable
	form_class = LinkTypeSearchForm
	context_table_name = 'links'
	checkbox_object_name = 'link'
	actions = ('make_visible', 'make_invisible', )
	template_name = 'dashboard/linktype/linktype_list.html'

	def dispatch(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		self.form = self.get_form(form_class)
		return super(LinkTypeListView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(LinkTypeListView, self).get_form_kwargs()
		if 'search' in self.request.GET:
			kwargs.update({
				'data': self.request.GET,
			})
		return kwargs

	def get_context_data(self, **kwargs):
		ctx = super(LinkTypeListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Social media search results')
		return _('Social media')

	def get_table(self, **kwargs):
		table = super(LinkTypeListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_queryset(self):
		queryset = self.model.objects.all()
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['name']:
			queryset = queryset.filter(name__icontains=data['name'])
		return queryset

	def make_invisible(self, request, links):
		return self._change_link_visible_status(links, False)

	def make_visible(self, request, links):
		return self._change_link_visible_status(links, True)

	def _change_link_visible_status(self, links, value):
		for link in links:
			link.is_visible = value
			link.save()
		messages.info(self.request, _("Link status successfully changed"))
		return redirect('link-list')


	
class LinkTypeDetailView(DetailView):
	model = LinkType
	context_object_name = 'txn'
	template_name = 'dashboard/linktype/linktype_detail.html'

class LinkTyCreateView(CreateView):
	model = LinkType
	form_class = LinkTypeForm
	template_name = 'dashboard/linktype/linktype_form.html'

	def get_success_url(self):
		messages.info(self.request, _("Social media created successfully"))
		return super(LinkTyCreateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(LinkTyCreateView, self).get_context_data(**kwargs)
		ctx['title'] = _("Create social media")
		return ctx

class LinkTypeUpdateView(UpdateView):
	model = LinkType
	form_class = LinkTypeForm
	template_name = 'dashboard/linktype/linktype_form.html'

	def get_success_url(self):
		messages.info(self.request, _("Social media updated successfully"))
		return super(LinkTypeUpdateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(LinkTypeUpdateView, self).get_context_data(**kwargs)
		ctx['link'] = self.object
		ctx['title'] = self.object.name
		return ctx

class LinkTypeDeleteView(DeleteView):
	model = LinkType
	context_object_name = 'social'
	template_name = 'dashboard/linktype/linktype_delete.html'

	def get_success_url(self):
		messages.info(self.request, _("Social media deleted"))
		return reverse('link-list')