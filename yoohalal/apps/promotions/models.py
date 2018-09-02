from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model
from oscar.apps.promotions.models import AbstractProductList, AutomaticProductList


class CategoryProductList(AbstractProductList):
    _type = 'Category-product list'
    category = models.ForeignKey(
        'catalogue.Category',
        on_delete=models.CASCADE,
        verbose_name=_("Category"))

    num_products = models.PositiveSmallIntegerField(_('Number of Products'),
                                                    default=4)
             
    def get_queryset(self):
        Product = get_model('catalogue', 'Product')
        qs = Product.browsable.base_queryset().filter(categories=self.category)
        return qs

    def get_products(self):
        return self.get_queryset().filter(status='publish')[:self.num_products]

    class Meta:
        app_label = 'promotions'
        verbose_name = _("Category product list")
        verbose_name_plural = _("Category product lists")


class  AutomaticProductList(AutomaticProductList):

    def get_products(self):
        return self.get_queryset().filter(status='publish')[:self.num_products]