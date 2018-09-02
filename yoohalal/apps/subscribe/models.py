import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


def _make_uuid():
	return str(uuid.uuid4())


@python_2_unicode_compatible
class SubscribeBase(models.Model):
	reference = models.CharField(_('Reference'), max_length=100, blank=True, unique=True, default=_make_uuid)
	email = models.EmailField(_('Email Address'), max_length=254)
	is_active = models.BooleanField(_('is active'), default=True)
	date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)

	class Meta:
		app_label = 'subscribe'
		ordering = ('email',)
		verbose_name = _('subscribe')
		verbose_name_plural = _('subscribes')

	def __str__(self):
		return self.email