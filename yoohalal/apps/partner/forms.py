from django import forms
from django.utils.translation import pgettext_lazy
from oscar.views.generic import PhoneNumberMixin

from oscar.core.loading import get_class, get_model

from apps.customer.utils import Dispatcher


PartnerAddress = get_model('partner', 'PartnerAddress')
Country = get_model('address', 'Country')
CommunicationEventType = get_model('customer', 'CommunicationEventType')


class PartnerAddressForm(PhoneNumberMixin, forms.ModelForm):
    name = forms.CharField(
        required=False, max_length=128,
        label=pgettext_lazy(u"Partner's name", u"Name"))

    def __init__(self, *args, **kwargs):
        super(PartnerAddressForm, self).__init__(*args, **kwargs)
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

    def send_email(self, site, sender, partner):
        ctx = {'partner':partner, 'site':site, 'sender':sender}

        try:
            event_type = CommunicationEventType.objects.get(code='PARTNER_REGISTER')
        except CommunicationEventType.DoesNotExist:
            messages = CommunicationEventType.objects.get_and_render('PARTNER_REGISTER', ctx)
        else:
            messages = event_type.get_messages(ctx)

        if messages and messages['body']:
            Dispatcher().send_random_email_messages(messages, sender)

    class Meta:
        fields = ('name', 'full_address', 'sub_districts', 'city',
                  'state', 'postcode', 'country',)
        model = PartnerAddress