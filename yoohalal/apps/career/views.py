from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.views import View

from oscar.core.loading import get_class, get_model

Applicant = get_model('career', 'Applicant')
Career = get_model('career', 'Career')
ApplicantForm = get_class('career.forms', 'ApplicantForm')


class ApplicantView(FormView):
	form_class = ApplicantForm
	template_name = 'career/applicant_form.html'

	def get_form_kwargs(self):
		kwargs = super(ApplicantView, self).get_form_kwargs()
		if 'career_id' in self.kwargs:
			career = Career.objects.get(pk=self.kwargs['career_id'])
			if career:
				self.career = career
				kwargs['instance'] = Applicant(
										career=career
									 )
		return kwargs

	def get_context_data(self, **kwargs):
		ctx = super(ApplicantView, self).get_context_data(**kwargs)
		ctx['career'] = self.career
		return ctx

	def get_success_url(self, **kwargs):
		return reverse('career:applicant-thanks', kwargs={'ref': kwargs['reference'],
													'career_id': kwargs['career_id']})

	def form_valid(self, form):
		applicant = form.save()
		return HttpResponseRedirect(self.get_success_url(reference=applicant.reference,
														career_id=applicant.career_id))


class ThanksView(DetailView):
	template_name = 'career/applicant_thanks.html'
	context_object_name = 'obj'
	model = Applicant

	def get(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
		except Http404:
			return reverse('career:applicant-form', kwargs={'career_id': self.kwargs['career_id']})
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		ctx = super(ThanksView, self).get_context_data(**kwargs)
		career = Career.objects.get(pk=self.object.career_id)
		if career:
			ctx['career'] = career
		return ctx

	def get_object(self):
		obj = get_object_or_404(Applicant,reference=self.kwargs['ref'])
		return obj


class CareerListView(ListView):
	model = Career
	context_object_name = 'careers'
	template_name = 'career/career_index.html'
	queryset = Career.objects.published().all()
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(CareerListView, self).get_context_data(**kwargs)
		context['title'] = _('Career')
		return context


class CareerDetailView(DetailView):
	model = Career
	template_name = 'career/career_detail.html'
	context_object_name = 'career'

	def get(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
		except Http404:
			return redirect('career:career-list')
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_object(self):
		career = get_object_or_404(Career,slug=self.kwargs['slug'])
		return career

	def get_context_data(self, **kwargs):
		context = super(CareerDetailView, self).get_context_data(**kwargs)
		career = self.get_object()
		context["title"] = career.title
		return context

