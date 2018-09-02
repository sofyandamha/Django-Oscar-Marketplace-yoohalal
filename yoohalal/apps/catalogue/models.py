
from decimal import Decimal as D
from decimal import InvalidOperation

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from babel.numbers import format_currency
from django.utils.translation import get_language, to_locale

from oscar.core.loading import get_class, get_model
from oscar.apps.partner.strategy import Default

from meta.models import ModelMeta
from meta import settings as MetaSettings

AbstractProduct = get_class('catalogue.abstract_models', 'AbstractProduct')


class Product(ModelMeta, AbstractProduct):
	status = models.CharField(
		_("Status"), max_length=50, choices=settings.PRODUCT_STATUS,
		default='draft')

	_metadata = {
		'title': 'title',
		'description': 'get_description',
		'url': 'get_absolute_url',
		'image': 'get_meta_image',
		'og_type': 'product',
		'og_description': 'get_description',
		'gplus_type': 'product',
		'gplus_description': 'get_description',
		'twitter_type': 'product',
		'twitter_description': 'get_description',
		'twitter_creator': '@yoohalal',
		'twitter_site': '@yoohalal',
		'extra_props': 'get_extra_props',
	}

	def get_description(self):
		return strip_tags(self.description)

	def get_meta_image(self):
		image = self.primary_image()
		if image:
			return image.original.url

	def get_extra_props(self):
		return {
			'twitter:data1': self.get_price_for_meta(),
			'twitter:label1': 'Harga',
			'twitter:data2': self.get_partner_location(),
			'twitter:label2': 'Lokasi',
		}

	def get_partner_location(self):
		location = 'Jakarta'

		d = Default()
		session = d.fetch_for_product(product=self)
		if self.is_parent:
			session = d.fetch_for_parent(product=self)

		if session.stockrecord:
			if session.stockrecord.partner.primary_address:
				return session.stockrecord.partner.primary_address.city
		
		return location

	def get_price_for_meta(self):
		harga = 'Rp 0'
		d = Default()
		session = d.fetch_for_product(product=self)
		if self.is_parent:
			session = d.fetch_for_parent(product=self)

		if session.price.exists and session.price.excl_tax != 0:
			if session.price.is_tax_known:
				harga = self.get_price_with_format(session.price.incl_tax, session.price.currency)
			else:
				harga = self.get_price_with_format(session.price.excl_tax, session.price.currency)

		return harga

	def get_price_with_format(self, harga, currency=None):
	    try:
	        value = D(harga)
	    except (TypeError, InvalidOperation):
	        return u""

	    OSCAR_CURRENCY_FORMAT = getattr(settings, 'OSCAR_CURRENCY_FORMAT', None)
	    kwargs = {
	    	'currency': currency or settings.OSCAR_DEFAULT_CURRENCY,
	    	'locale': to_locale(get_language() or settings.LANGUAGE_CODE)
	    }
	    if isinstance(OSCAR_CURRENCY_FORMAT, dict):
	        kwargs.update(OSCAR_CURRENCY_FORMAT.get(currency, {}))
	    else:
	        kwargs['format'] = OSCAR_CURRENCY_FORMAT

	    return format_currency(value, **kwargs)


from oscar.apps.catalogue.models import *