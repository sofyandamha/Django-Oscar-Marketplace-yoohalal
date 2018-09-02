from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_class, get_model
from oscar.apps.dashboard.catalogue.forms import ProductForm, ProductSearchForm

StockRecord = get_model('partner', 'StockRecord')
Partner = get_model('partner', 'Partner')
Category = get_model('catalogue', 'Category')
ProductClass = get_model('catalogue', 'ProductClass')


class StockRecordForm(forms.ModelForm):

    def __init__(self, product_class, user, *args, **kwargs):
        # The user kwarg is not used by stock StockRecordForm. We pass it
        # anyway in case one wishes to customise the partner queryset
        self.user = user
        super(StockRecordForm, self).__init__(*args, **kwargs)

        self.fields['partner'].queryset = Partner.objects.filter(is_active=True)

        # Restrict accessible partners for non-staff users
        if not self.user.is_staff:
            self.fields['partner'].queryset = Partner.objects.filter(user_id=self.user.id, is_active=True)

        # If not tracking stock, we hide the fields
        if not product_class.track_stock:
            for field_name in ['num_in_stock', 'low_stock_treshold']:
                if field_name in self.fields:
                    del self.fields[field_name]
        else:
            for field_name in ['price_excl_tax', 'num_in_stock']:
                if field_name in self.fields:
                    self.fields[field_name].required = True

    class Meta:
        model = StockRecord
        fields = [
            'partner', 'partner_sku',
            'price_currency', 'price_excl_tax', 'old_price', 'price_retail', 'cost_price',
            'num_in_stock', 'low_stock_threshold',
        ]

class ProductForm(ProductForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProductForm, self).__init__(*args, **kwargs)
        if not self.user.is_staff:
            self.fields.pop('status')

    def add_attribute_fields(self, product_class, is_parent=False):
        """
        For each attribute specified by the product class, this method
        dynamically adds form fields to the product form.
        """
        for attribute in product_class.attributes.all():
            field = self.get_attribute_field(attribute)
            if field:
                if attribute.code == 'weight':
                    self.fields['attr_%s' % attribute.code] = field
                    self.fields['attr_%s' % attribute.code].help_text = _("weight in grams")
                    # Attributes are not required for a parent product
                    if is_parent:
                        self.fields['attr_%s' % attribute.code].required = False
                else:
                    self.fields['attr_%s' % attribute.code] = field
                    # Attributes are not required for a parent product
                    if is_parent:
                        self.fields['attr_%s' % attribute.code].required = False

    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields + ['status']


class ProductSearchForm(ProductSearchForm):
    product_type = forms.ModelChoiceField(
        label=_("Product Type"), required=False, queryset=ProductClass.objects.all())

    category = forms.ModelChoiceField(
        label=_("Category"), required=False, queryset=Category.objects.all())

    partner = forms.ModelChoiceField(
        label=_("Partner"), required=False, queryset=Partner.objects.filter(is_active=True))