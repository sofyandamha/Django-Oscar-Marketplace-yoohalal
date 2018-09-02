from haystack import indexes

from oscar.apps.search.search_indexes import ProductIndex


class ProductIndex(ProductIndex):
	status = indexes.CharField(model_attr="status", null=True)

	def index_queryset(self, using=None):
		return super(ProductIndex, self).index_queryset().filter(status='publish')

	def read_queryset(self, using=None):
		return super(ProductIndex, self).read_queryset().filter(status='publish')