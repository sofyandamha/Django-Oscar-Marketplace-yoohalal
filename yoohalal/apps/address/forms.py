from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_model
from oscar.apps.address.forms import *

Country = get_model('address', 'Country')

class UserAddressForm(UserAddressForm):

    class Meta(UserAddressForm.Meta):
        fields = ['full_name', 'full_address', 'sub_districts', 'city'] + UserAddressForm.Meta.fields 

    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        for field in ['title', 'first_name', 'last_name', 'line1', 'line2', 'line3', 'line4']:
            self.fields.pop(field)
        self.fields['phone_number'].label = _('Phone number')
        self.fields['full_address'].widget.attrs['rows'] = 3
        self.adjust_country_field()
    
    def adjust_country_field(self):
        countries = Country._default_manager.filter(
            is_shipping_country=True)

        # No need to show country dropdown if there is only one option
        if len(countries) == 1:
            self.fields.pop('country', None)
            self.instance.country = countries[0]
        else:
            self.fields['country'].queryset = countries
            self.fields['country'].empty_label = None