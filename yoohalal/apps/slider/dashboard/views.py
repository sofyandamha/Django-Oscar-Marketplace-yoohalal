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

from .tables import SliderImageTable
from .forms import SliderSearchForm

SliderImage = get_model('slider', 'SliderImage')
SliderForm = get_class('slider.forms', 'SliderForm')


class SliderListView(BulkEditMixin, FormMixin, SingleTableView):
	model = SliderImage
	table_pagination = True
	table_class = SliderImageTable
	form_class = SliderSearchForm
	context_table_name = 'sliders'
	checkbox_object_name = 'image'
	actions = ('make_visible', 'make_invisible', )
	template_name = 'dashboard/slider/slider_list.html'

	def dispatch(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		self.form = self.get_form(form_class)
		return super(SliderListView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(SliderListView, self).get_form_kwargs()
		if 'search' in self.request.GET:
			kwargs.update({
				'data': self.request.GET,
			})
		return kwargs

	def get_context_data(self, **kwargs):
		ctx = super(SliderListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Sliders search results')
		return _('Sliders')

	def get_table(self, **kwargs):
		table = super(SliderListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_queryset(self):
		queryset = self.model.objects.all()
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['slider_number']:
			queryset = queryset.filter(slider_number=data['slider_number'])
		if data['is_visible']:
			queryset = queryset.filter(is_visible=data['is_visible'])
		return queryset

	def make_invisible(self, request, sliders):
		return self._change_link_visible_status(sliders, False)

	def make_visible(self, request, sliders):
		return self._change_link_visible_status(sliders, True)

	def _change_link_visible_status(self, sliders, value):
		for slider in sliders:
			slider.is_visible = value
			slider.save()
		messages.info(self.request, _("Slider status successfully changed"))
		return redirect('slider-list')
	

class SliderDetailView(DetailView):
	model = SliderImage
	context_object_name = 'txn'
	template_name = 'dashboard/slider/slider_detail.html'


class SliderCreateView(CreateView):
	model = SliderImage
	form_class = SliderForm
	template_name = 'dashboard/slider/slider_form.html'

	def get_success_url(self):
		messages.info(self.request, _("Slider created successfully"))
		return super(SliderCreateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(SliderCreateView, self).get_context_data(**kwargs)
		ctx['title'] = _("Create slider")
		return ctx


class SliderUpdateView(UpdateView):
	model = SliderImage
	form_class = SliderForm
	template_name = 'dashboard/slider/slider_form.html'

	def get_success_url(self):
		messages.info(self.request, _("Slider updated successfully"))
		return super(SliderUpdateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(SliderUpdateView, self).get_context_data(**kwargs)
		ctx['slider'] = self.object
		ctx['title'] = self.object.image.name
		return ctx


class SliderDeleteView(DeleteView):
	model = SliderImage
	context_object_name = 'slider'
	template_name = 'dashboard/slider/slider_delete.html'

	def get_success_url(self):
		messages.info(self.request, _("Slider deleted"))
		return reverse('slider-list')