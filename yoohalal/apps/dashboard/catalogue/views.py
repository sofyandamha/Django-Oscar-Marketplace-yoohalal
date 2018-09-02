from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model
from oscar.apps.dashboard.catalogue.views import (
	ProductListView, ProductCreateUpdateView, ProductDeleteView, ProductLookupView)

from apps.dashboard.catalogue.formsets import StockRecordFormSet

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductCategory = get_model('catalogue', 'ProductCategory')


def filter_products(queryset, user):
	if user.is_staff:
		return queryset
	return queryset.filter(stockrecords__partner__user_id=user.pk).distinct()


class ProductListView(ProductListView):
	template_name = 'dashboard/catalogue/product_list.html'
	context_table_name = 'products'

	def get_context_data(self, **kwargs):
		ctx = super(ProductListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		ctx['productclass_form'] = self.productclass_form_class()
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Product search results')
		return _('Products')

	def get_table(self, **kwargs):
		if 'recently_edited' in self.request.GET:
			kwargs.update(dict(orderable=False))

		table = super(ProductListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def filter_queryset(self, queryset):
		return filter_products(queryset, self.request.user)

	def get_queryset(self):
		queryset = Product.browsable.base_queryset()
		queryset = self.filter_queryset(queryset)
		queryset = self.apply_search(queryset)
		return queryset

	def apply_search(self, queryset):
		self.form = self.form_class(self.request.GET)

		if not self.form.is_valid():
			return queryset

		data = self.form.cleaned_data

		if data.get('product_type'):
			queryset = queryset.filter(product_class__name=data['product_type'])

		if data.get('category'):
			queryset = queryset.filter(categories__name=data['category'])

		if data.get('partner'):
			queryset = queryset.filter(stockrecords__partner=data['partner'])

		if data.get('upc'):
			matches_upc = Product.objects.filter(upc=data['upc'])
			qs_match = queryset.filter(
				Q(id__in=matches_upc.values('id')) |
				Q(id__in=matches_upc.values('parent_id')))

			if qs_match.exists():
				queryset = qs_match
			else:
				matches_upc = Product.objects.filter(upc__icontains=data['upc'])
				queryset = queryset.filter(
					Q(id__in=matches_upc.values('id')) | Q(id__in=matches_upc.values('parent_id')))

		if data.get('title'):
			queryset = queryset.filter(title__icontains=data['title'])

		return queryset


class ProductCreateUpdateView(ProductCreateUpdateView):
	stockrecord_formset = StockRecordFormSet

	def get_queryset(self):
		return filter_products(Product.objects.all(), self.request.user)

	def get_form_kwargs(self):
		kwargs = super(ProductCreateUpdateView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs


class ProductDeleteView(ProductDeleteView):

	def get_queryset(self):
		return filter_products(Product.objects.all(), self.request.user)


class ProductLookupView(ProductLookupView):

	def get_queryset(self):
		return self.model.browsable.all().filter(status='publish')