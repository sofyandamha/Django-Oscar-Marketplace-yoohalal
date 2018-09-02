import logging

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from oscar.core.loading import get_class, get_model
from oscar.apps.customer.utils import *

class Dispatcher(Dispatcher):
	def send_random_email_messages(self, messages, sender):

		if hasattr(settings, 'OSCAR_FROM_EMAIL'):
			recipient = settings.OSCAR_FROM_EMAIL
		else:
			recipient = None

		if messages['subject'] and (messages['body'] or messages['html']):
			if messages['html']:
				email = EmailMultiAlternatives(messages['subject'],
											   messages['body'],
											   from_email=sender,
											   to=[recipient])
				email.attach_alternative(messages['html'], "text/html")
			else:
				email = EmailMessage(messages['subject'],
									 messages['body'],
									 from_email=sender,
									 to=[recipient])
			self.logger.info("Sending email to %s" % recipient)

			if self.mail_connection:
				self.mail_connection.send_messages([email])
			else:
				email.send()

			return email


class TokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
		)

account_activation_token = TokenGenerator()