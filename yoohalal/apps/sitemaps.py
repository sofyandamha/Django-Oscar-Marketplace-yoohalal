# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.utils.translation import get_language, activate
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')

from apps.blog.models import PostEntry
from apps.career.models import Career
from django.utils import timezone

"""
A basic example what a sitemap could look like for a multi-language Oscar
instance.
Creates entries for the homepage, for each product and each category.
Repeats those for each enabled language.
"""


class I18nSitemap(Sitemap):
    """
    A language-specific Sitemap class. Returns URLS for items for passed
    language.
    """
    def __init__(self, language):
        self.language = language
        self.original_language = get_language()

    def get_obj_location(self, obj):
        return obj.get_absolute_url()

    def location(self, obj):
        activate(self.language)
        location = self.get_obj_location(obj)
        activate(self.original_language)
        return location

class StaticSitemap(I18nSitemap):

    def items(self):
        return ['promotions:home',]

    def get_obj_location(self, obj):
        return reverse(obj)


class ProductSitemap(I18nSitemap):

    def items(self):
        qs = Product.browsable.base_queryset()
        return qs.filter(status='publish')

class CategorySitemap(I18nSitemap):

    def items(self):
        return Category.objects.all()


class BlogSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return PostEntry.objects.filter(published=True)

    def lastmod(self, item):
        return item.created

class CareerSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Career.objects.all()

    def lastmod(self, item):
        return item.date_published


language_neutral_sitemaps = {
    'static': StaticSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blogs': BlogSitemap,
    'career': CareerSitemap,
}

# Construct the sitemaps for every language
base_sitemaps = {}
for language, __ in settings.LANGUAGES:
    for name, sitemap_class in language_neutral_sitemaps.items():
        base_sitemaps['{0}-{1}'.format(name, language)] = sitemap_class(language)
