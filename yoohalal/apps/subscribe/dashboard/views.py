from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormMixin

from oscar.apps.customer.utils import normalise_email
from oscar.views.generic import BulkEditMixin
from oscar.core.loading import get_class, get_model

from django_tables2 import SingleTableView

from .tables import SubscribeTable
from .forms import SubscribeSearchForm

SubscribeBase = get_model('subscribe', 'SubscribeBase')


class SubscribeListView(BulkEditMixin, FormMixin, SingleTableView):
	model = SubscribeBase
	table_pagination = True
	table_class = SubscribeTable
	form_class = SubscribeSearchForm
	context_table_name = 'subscribes'
	checkbox_object_name = 'subscribe'
	actions = ('make_active', 'make_inactive', )
	template_name = 'dashboard/subscribe/subscribe_list.html'

	def dispatch(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		self.form = self.get_form(form_class)
		return super(SubscribeListView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(SubscribeListView, self).get_form_kwargs()
		if 'search' in self.request.GET:
			kwargs.update({
				'data': self.request.GET,
			})
		return kwargs

	def get_context_data(self, **kwargs):
		ctx = super(SubscribeListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Subscribes search results')
		return _('Subscribes')

	def get_table(self, **kwargs):
		table = super(SubscribeListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_queryset(self):
		queryset = self.model.objects.all()
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['email']:
			email = normalise_email(data['email'])
			queryset = queryset.filter(email__istartswith=email)
		return queryset

	def make_inactive(self, request, subscribes):
		return self._change_subscriber_active_status(subscribes, False)

	def make_active(self, request, subscribes):
		return self._change_subscriber_active_status(subscribes, True)

	def _change_subscriber_active_status(self, subscribes, value):
		for subscribe in subscribes:
			subscribe.is_active = value
			subscribe.save()
		messages.info(self.request, _("Subscriber status successfully changed"))
		return redirect('subscribe-list')

	
class SubscribeDetailView(DetailView):
	model = SubscribeBase
	context_object_name = 'txn'
	template_name = 'dashboard/subscribe/subscribe_detail.html'
