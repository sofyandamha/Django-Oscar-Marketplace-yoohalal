from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.views import View

from .forms import SubscribeForm
from .models import SubscribeBase


def post_subscribe(request):
	if request.method == 'POST':
		form = SubscribeForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get("email", "")
			subscrip, created = SubscribeBase.objects.get_or_create(email=email)

			if not subscrip.is_active:
				subscrip.is_active = True
				subscrip.save()

			form.send_email(get_current_site(request), subscrip.email, subscrip.reference)
			return HttpResponseRedirect(reverse('subscribe:subscribe-thanks', kwargs={'ref': subscrip.reference}))
	else:
		form = SubscribeForm()

	return HttpResponseRedirect(reverse('promotions:home'))


def unsubscribe(request, ref):
	try:
		subscrip = SubscribeBase.objects.get(reference=ref)
		subscrip = SubscribeBase.objects.update(is_active=False)
	except SubscribeBase.DoesNotExist:
		return HttpResponseRedirect(reverse('promotions:home'))
		
		subscrip.save()

	return render(request, 'subscribe/unsubscribe.html')


class SubscribeView(FormView):
	form_class = SubscribeForm
	template_name = 'subscribe/subscribe_form.html'

	def get_success_url(self, **kwargs):
		return reverse('subscribe:subscribe-thanks', kwargs={'ref': kwargs['reference']})

	def form_valid(self, form):
		email = form.cleaned_data.get("email", "")
		subscrip, created = SubscribeBase.objects.get_or_create(email=email)

		if not subscrip.is_active:
			subscrip.is_active = True
			subscrip.save()

		form.send_email(get_current_site(self.request), subscrip.email, subscrip.reference)
		return HttpResponseRedirect(self.get_success_url(reference = subscrip.reference))


class ThanksView(DetailView):
	template_name = 'subscribe/thanks.html'
	context_object_name = 'obj'
	model = SubscribeBase

	def get(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
		except Http404:
			return reverse('subscribe:subscribe-form')
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_object(self):
		obj = get_object_or_404(SubscribeBase,reference=self.kwargs['ref'])
		return obj