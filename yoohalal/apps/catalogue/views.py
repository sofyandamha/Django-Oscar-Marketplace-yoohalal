from oscar.core.loading import get_class, get_model
from oscar.apps.catalogue.views import ProductDetailView

from meta.views import MetadataMixin


class ProductDetailView(ProductDetailView):
   
	def get_context_data(self, **kwargs):
		ctx = super(ProductDetailView, self).get_context_data(**kwargs)
		ctx['meta'] = self.get_object().as_meta()
		return ctx