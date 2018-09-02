import os
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.core.urlresolvers import reverse
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField

from apps.career.utils import file_cleanup


def _make_uuid():
	return str(uuid.uuid4())


class Applicant(models.Model):
	reference = models.CharField(_('Reference'), max_length=100, blank=True,
						unique=True, default=_make_uuid)
	name = models.CharField(_('Full Name'), max_length=100)
	email = models.EmailField(_('Email'), max_length=100)
	phone_number = PhoneNumberField(_('Phone number'), blank=True)
	document = models.FileField(
					_('Document'), upload_to=settings.CAREER_DOCUMENT_FOLDER,
					validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
	date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
	country = models.ForeignKey(
		'address.Country',
		on_delete=models.CASCADE,
		verbose_name=_("Country"))
	career = models.ForeignKey(
		'career.Career',
		on_delete=models.CASCADE,
		verbose_name=_("Career"))

	class Meta:
		app_label = 'career'
		ordering = ['name']
		verbose_name = _('Applicant')
		verbose_name_plural = _('Applicants')

	@property
	def filename(self):
		return os.path.basename(self.document.name)


post_delete.connect(file_cleanup, sender=Applicant, dispatch_uid='Applicant.file_cleanup')


class Departement(models.Model):
	departement = models.CharField(_('Departement'), max_length=100, unique=True)
	slug = models.CharField(max_length=150, unique=True)

	def __str__(self):
		return self.departement

	def get_absolute_url(self):
		return reverse('departement-list')

	def _get_unique_slug(self, slug):
		unique_slug = slug
		num = 1
		while Departement.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		slug = slugify(self.departement)
		if not self.slug or self.slug != slug:
		   self.slug = self._get_unique_slug(slug)
		return super(Departement, self).save(*args, **kwargs)

	class Meta:
		app_label = 'career'
		ordering = ['departement']
		verbose_name = _('Department')
		verbose_name_plural = _('Departments')


class CareerQuery(models.QuerySet):

	def published(self):
		return self.filter(published=True)


class Career(models.Model):
	title = models.CharField(_('Title'), max_length=200)
	slug = models.SlugField(max_length=225, unique=True)
	body = models.TextField(_('Body'), blank=True)
	date_published = models.DateTimeField(_('Date Published'), default=timezone.now)
	published = models.BooleanField(_('Published'), default=True)
	departement = models.ForeignKey('career.Departement', on_delete=models.CASCADE,
							verbose_name=_("Departement"))
	objects = CareerQuery.as_manager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('career:career-detail', kwargs={'slug': self.slug}) 

	def _get_unique_slug(self, slug):
		unique_slug = slug
		num = 1
		while Career.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		slug = slugify(self.title)
		if not self.slug or self.slug != slug:
		   self.slug = self._get_unique_slug(slug)
		return super(Career, self).save(*args, **kwargs)

	class Meta:
		app_label = 'career'
		ordering = ['-date_published']
		verbose_name = _('Career')
		verbose_name_plural = _('Careers')
