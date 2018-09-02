import logging

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode

from oscar.apps.customer.signals import user_registered
from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_model
from oscar.apps.customer.mixins import RegisterUserMixin

from .utils import account_activation_token

User = get_user_model()
CommunicationEventType = get_model('customer', 'CommunicationEventType')
Dispatcher = get_class('customer.utils', 'Dispatcher')

logger = logging.getLogger('oscar.customer')


class RegisterUserMixin(RegisterUserMixin):

    def register_user(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        user_registered.send_robust(
            sender=self, request=self.request, user=user)

        if getattr(settings, 'OSCAR_SEND_REGISTRATION_EMAIL', True):
            self.send_registration_email(user)

        try:
            user = authenticate(
                username=user.email,
                password=form.cleaned_data['password1'])
        except User.MultipleObjectsReturned:
            logger.warning(
                'Multiple users with identical email address and password'
                'were found. Marking all but one as not active.')
            users = User.objects.filter(email=user.email)
            user = users[0]
            for u in users[1:]:
                u.is_active = False
                u.save()

        # auth_login(self.request, user)

        return user

    def send_registration_email(self, user):
        code = self.communication_type_code
        ctx = {'user': user,
               'site': get_current_site(self.request),
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': account_activation_token.make_token(user)}
        messages = CommunicationEventType.objects.get_and_render(
            code, ctx)
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(user, messages)
