from django.core import exceptions
from oscar.core.loading import get_classes, get_model
from django.forms.models import inlineformset_factory
from oscar.apps.dashboard.catalogue.formsets import StockRecordFormSet

from .forms import StockRecordForm

Product = get_model('catalogue', 'Product')
StockRecord = get_model('partner', 'StockRecord')
Partner = get_model('partner', 'Partner')

(ProductCategoryForm,
ProductImageForm,
ProductRecommendationForm,
ProductAttributesForm) = \
    get_classes('dashboard.catalogue.forms',
                ('ProductCategoryForm',
                 'ProductImageForm',
                 'ProductRecommendationForm',
                 'ProductAttributesForm'))


BaseStockRecordFormSet = inlineformset_factory(
    Product, StockRecord, form=StockRecordForm, extra=1)


class StockRecordFormSet(BaseStockRecordFormSet):

    def __init__(self, product_class, user, *args, **kwargs):
        self.user = user
        self.require_user_stockrecord = not user.is_staff
        self.product_class = product_class

        if not user.is_staff and \
           'instance' in kwargs and \
           'queryset' not in kwargs:
            kwargs.update({
                'queryset': StockRecord.objects.filter(product=kwargs['instance'],
                                                       partner__in=Partner.objects.filter(user_id=user.id))
            })

        super(StockRecordFormSet, self).__init__(*args, **kwargs)
        self.set_initial_data()

    def set_initial_data(self):
        if self.require_user_stockrecord:
            try:
                user_partner = self.user.partner
            except (exceptions.ObjectDoesNotExist,
                    exceptions.MultipleObjectsReturned):
                pass
            else:
                partner_field = self.forms[0].fields.get('partner', None)
                if partner_field and partner_field.initial is None:
                    partner_field.initial = user_partner

    def _construct_form(self, i, **kwargs):
        kwargs['product_class'] = self.product_class
        kwargs['user'] = self.user
        return super(StockRecordFormSet, self)._construct_form(
            i, **kwargs)

    def clean(self):
        if any(self.errors):
            return
        if self.require_user_stockrecord:
            stockrecord_partners = set([form.cleaned_data.get('partner', None)
                                        for form in self.forms])
            user_partners = set(Partner.objects.filter(user_id=self.user.id))
            if not user_partners & stockrecord_partners:
                raise exceptions.ValidationError(
                    _("At least one stock record must be set to a partner that"
                      " you're associated with."))