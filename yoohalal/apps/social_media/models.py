from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.text import slugify

class LinkType(models.Model):

	name = models.CharField(_('Name'), max_length=100)
	slug = models.SlugField(_('Slug'), max_length=100, unique=True)
	url = models.CharField(_('Url'), max_length=4000)
	is_visible = models.BooleanField(_('Is Visible'), default=True)
	order_number = models.IntegerField(_('Position Number'), default=1)

	def __unicode__(self):
		return self.name

	def get_absolute_url(self): 
		return reverse('link-list') 

	def _get_unique_slug(self, slug):
		unique_slug = slug
		num = 1
		while LinkType.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug
 
	def save(self, *args, **kwargs):
		slug = slugify(self.name)
		if not self.slug or self.slug != slug:
		   self.slug = self._get_unique_slug(slug)

		return super(LinkType, self).save(*args, **kwargs)