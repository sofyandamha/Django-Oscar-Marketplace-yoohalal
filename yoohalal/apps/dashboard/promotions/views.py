import itertools

from django.views import generic
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


from oscar.core.loading import get_class, get_classes
from oscar.apps.dashboard.promotions.views import (ListView,
    CreateRedirectView, CreateView, UpdateView, DeleteView)

from apps.promotions.conf import PROMOTION_CLASSES

CategoryProductList = get_class('apps.promotions.models', 'CategoryProductList')
SelectForm = get_class('apps.dashboard.promotions.forms', 'PromotionTypeSelectForm')


class ListView(ListView):

    def get_context_data(self):
        data = []
        num_promotions = 0
        for klass in PROMOTION_CLASSES:
            objects = klass.objects.all()
            num_promotions += objects.count()
            data.append(objects)
        promotions = itertools.chain(*data)
        ctx = {
            'num_promotions': num_promotions,
            'promotions': promotions,
            'select_form': SelectForm(),
        }
        return ctx


class CreateRedirectView(CreateRedirectView):

    def get_redirect_url(self, **kwargs):
        code = self.request.GET.get('promotion_type', None)
        urls = {}
        for klass in PROMOTION_CLASSES:
            urls[klass.classname()] = reverse('dashboard:promotion-create-%s' %
                                              klass.classname())
        return urls.get(code, None)


class CreateCategoryProductListView(CreateView):
    model = CategoryProductList
    fields = ['name', 'description', 'link_url', 'link_text', 'category',
              'num_products']


class UpdateCategoryProductListView(UpdateView):
    model = CategoryProductList
    fields = ['name', 'description', 'link_url', 'link_text', 'category',
              'num_products']


class DeleteCategoryProductListView(DeleteView):
    model = CategoryProductList