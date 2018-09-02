import random

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import post_delete, post_init, post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords

from .utils import file_cleanup
from meta.models import ModelMeta
from meta import settings as MetaSettings


class PostEntryQuery(models.QuerySet):
	def published(self):
		return self.filter(published=True)

	def randomPost(self):
		return self.published().order_by('?')[:4]

	def getFeaturedPost(self):
		return random.choice(self.published())


class PostTag(models.Model):
	tag = models.CharField(max_length=30)
	slug = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.tag

	class Meta:
		verbose_name = _('Tag')
		verbose_name_plural = _('Tags')
		ordering = ['tag']


class Category(models.Model):
	category = models.CharField(_('Category'), max_length=20, unique=True)
	slug = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.category

	def get_absolute_url(self):
		return reverse('category-list')

	def _get_unique_slug(self, slug):
		unique_slug = slug
		num = 1
		while Category.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		slug = slugify(self.category)
		if not self.slug or self.slug != slug:
		   self.slug = self._get_unique_slug(slug)

		return super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')
		ordering = ['category']


class PostEntry(ModelMeta, models.Model):
	title = models.CharField(_('Title'), max_length=200)
	image = models.ImageField(_('Image'), upload_to='blog/media/')
	post_body = models.TextField(_('Body'), blank=True)
	author = models.CharField(_('Author'), max_length=30)
	created = models.DateTimeField(_('Date Published'), default=timezone.now)
	slug = models.SlugField(max_length=200, unique=True)
	published = models.BooleanField(_('Published'), default=True)
	category = models.ForeignKey('blog.Category', on_delete=models.CASCADE, verbose_name=_("Category"))
	tags = models.ManyToManyField(PostTag)
	objects = PostEntryQuery.as_manager()

	_metadata = {
		'title': 'title',
		'description': 'get_description',
		'url': 'get_absolute_url',
		'image': 'get_meta_image',
		'og_type': 'article',
		'og_description': 'get_description',
		'gplus_type': 'article',
		'gplus_description': 'get_description',
		'twitter_type': 'article',
		'twitter_description': 'get_description',
		'twitter_creator': '@yoohalal',
		'twitter_site': '@yoohalal',
		'site_name': 'Yoohalal Blog',
		'published_time': 'created',
		'modified_time': 'get_date',
		'locale': 'ID',
		'tag': 'Index',
		'extra_props': 'get_extra_props',
	}

	def get_description(self):
		return truncatewords(strip_tags(self.post_body), 20)

	def get_meta_image(self):
			return self.image.url

	def get_date(self, param):
		if param == 'published_time':
			return self.created.strftime('%Y-%m-%dT%H:%M:%S:%z')
		elif param == 'modified_time':
			return self.created.strftime('%Y-%m-%dT%H:%M:%S:%z')
		return self.created

	def get_extra_props(self):
		return {
			'article:section': self.category,
		}

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.slug

	def get_absolute_url(self):
		return reverse('blog:blog-detail', kwargs={'slug': self.slug})

	def remove_on_image_update(self):
		try:
			obj = PostEntry.objects.get(id=self.id)
		except PostEntry.DoesNotExist:
			return

		if obj.image and self.image and obj.image != self.image:
			obj.image.delete()

	def _get_unique_slug(self, slug):
		unique_slug = slug
		num = 1
		while PostEntry.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		self.remove_on_image_update()

		slug = slugify(self.title)
		if not self.slug or self.slug != slug:
		   self.slug = self._get_unique_slug(slug)

		return super(PostEntry, self).save(*args, **kwargs)

	class Meta:
		verbose_name = _('Post')
		verbose_name_plural = _('Posts')
		ordering = ['-created',]

post_delete.connect(file_cleanup, sender=PostEntry, dispatch_uid='PostEntry.file_cleanup')