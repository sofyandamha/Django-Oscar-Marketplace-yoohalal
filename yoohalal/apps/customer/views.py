from django.conf import settings
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from oscar.core.compat import get_user_model, user_is_authenticated
from oscar.apps.customer.views import AccountAuthView

from .utils import account_activation_token

User = get_user_model()


class ActivateView(RedirectView):

	def get(self, request, *args, **kwargs):
		uidb64 = self.kwargs.get('uidb64', None)
		token = self.kwargs.get('token', None)

		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			# auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(self.request, _("Thank you for your email confirmation. Now you can login your account."))
			self.url = '/accounts/login/'
		else:
			messages.error(self.request, _("Activation link is invalid!"))
			self.url = '/accounts/login/'
		
		return super(ActivateView, self).get(request, args, **kwargs)


class AfterRegisterView(TemplateView):
	template_name = "customer/after_register.html"

	def get_context_data(self, **kwargs):
		context = super(AfterRegisterView, self).get_context_data(**kwargs)
		uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
		context['account'] = User.objects.get(pk=uid)
		return context


class AccountAuthView(AccountAuthView):
	
	def validate_registration_form(self):
		form = self.get_registration_form(bind_data=True)
		if form.is_valid():
			user = self.register_user(form)
			return redirect('customer:after-register', uidb64=urlsafe_base64_encode(force_bytes(user.pk)))

		ctx = self.get_context_data(registration_form=form)
		return self.render_to_response(ctx)