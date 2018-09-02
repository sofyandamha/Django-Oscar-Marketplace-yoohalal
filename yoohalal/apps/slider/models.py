from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse

from .utils import file_cleanup


class SliderImage(models.Model):
	image = models.ImageField(_('Image'), upload_to=settings.SLIDER_IMAGE_FOLDER)
	is_visible = models.BooleanField(_('Is Visible'), default=True)
	slider_number = models.IntegerField(_('Slider Number'), default=1)
	html_caption = models.TextField(_('Html Caption'), blank=True)

	class Meta:
		verbose_name = _('slider')
		verbose_name_plural = _('sliders')

	def __unicode__(self):
		return u"%d" % self.id

	def __str__(self):
		return self.image.name

	def get_absolute_url(self):
		return reverse('slider-list')

	def remove_on_image_update(self):
		try:
			obj = SliderImage.objects.get(id=self.id)
		except SliderImage.DoesNotExist:
			return

		if obj.image and self.image and obj.image != self.image:
			obj.image.delete()

	def save(self, *args, **kwargs):
		self.remove_on_image_update()
		return super(SliderImage, self).save(*args, **kwargs)

post_delete.connect(file_cleanup, sender=SliderImage, dispatch_uid='SliderImage.file_cleanup')