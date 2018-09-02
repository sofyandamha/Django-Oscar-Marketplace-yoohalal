from django.contrib import messages
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import FormView
from django.contrib.sites.shortcuts import get_current_site

from oscar.core.compat import get_user_model, user_is_authenticated
from oscar.core.loading import get_model

from .forms import PartnerAddressForm

User = get_user_model()
Partner = get_model('partner', 'Partner')
PartnerAddress = get_model('partner', 'PartnerAddress')


class PartnerRegistrationView(CreateView):
	template_name = 'partner/registration_form.html'
	form_class = PartnerAddressForm
	model = Partner

	def get(self, request, *args, **kwargs):
		if not user_is_authenticated(request.user):
			return redirect(settings.LOGIN_REDIRECT_URL)
		return super(PartnerRegistrationView, self).get(
			request, *args, **kwargs)

	def get_success_url(self, **kwargs):
		return reverse_lazy('partner:registration-success', kwargs = {'partner_id': kwargs['partner_id']})

	def form_valid(self, form):
		user = self.request.user

		if user.is_staff:
			messages.error(self.request, _("If you are a staff please use dashboard."))
			return redirect('partner:partner-registration')

		data = form.cleaned_data
		partner = Partner.objects.create(name=data['name'], user_id=user.id)
		address = PartnerAddress.objects.create(partner_id=partner.id, full_address=data['full_address'],
								 sub_districts=data['sub_districts'], city=data['city'],
								 state=data['state'], postcode=data['postcode'], country_id='ID',
								 phone_number=data['phone_number'])

		form.send_email(get_current_site(self.request), user.email, partner)

		return HttpResponseRedirect(self.get_success_url(partner_id=partner.id))


class RegistrationSuccessView(DetailView):
	template_name = 'partner/registration_success.html'
	context_object_name = 'partner'
	model = Partner

	def get(self, request, *args, **kwargs):
		if not user_is_authenticated(request.user):
			return redirect(settings.LOGIN_REDIRECT_URL)

		try:
			self.object = self.get_object()
		except Http404:
			return redirect('/partner/partner-registration/')

		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_object(self):
		obj = get_object_or_404(Partner,pk=self.kwargs['partner_id'])
		return obj