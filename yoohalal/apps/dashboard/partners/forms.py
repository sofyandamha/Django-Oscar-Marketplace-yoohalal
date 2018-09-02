from django import forms
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from oscar.apps.customer.forms import EmailUserCreationForm
from oscar.core.compat import existing_user_fields, get_user_model
from oscar.core.loading import get_model
from oscar.core.validators import validate_password

User = get_user_model()
Partner = get_model('partner', 'Partner')
PartnerAddress = get_model('partner', 'PartnerAddress')
Country = get_model('address', 'Country')


TRUE_FALSE_CHOICES = (
    (True, _('Yes')),
    (False, _('No'))
)

class PartnerCreateForm(forms.ModelForm):
    is_active = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label=_('Is Active?'), 
                                  initial=False, widget=forms.Select, required=True)

    def __init__(self, *args, **kwargs):
        super(PartnerCreateForm, self).__init__(*args, **kwargs)
        # Partner.name is optional and that is okay. But if creating through
        # the dashboard, it seems sensible to enforce as it's the only field
        # in the form.
        self.fields['name'].required = True

    class Meta:
        model = Partner
        fields = ('name', 'is_active', )


# ROLE_CHOICES = (
#     ('staff', _('Full dashboard access')),
#     ('limited', _('Limited dashboard access')),
# )

class NewUserForm(EmailUserCreationForm):
    # role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect,
    #                          label=_('User role'), initial='limited')

    def __init__(self, partner, *args, **kwargs):
        self.partner = partner
        super(NewUserForm, self).__init__(host=None, *args, **kwargs)

    def save(self):
        # role = self.cleaned_data.get('role', 'limited')
        user = super(NewUserForm, self).save(commit=False)

        # user.is_staff = role == 'staff'
        user.is_staff = False

        user.save()
        self.partner.user_id = user.id
        self.partner.save()

        # if role == 'limited':
        if self.partner.is_active:
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access', content_type__app_label='partner')
            user.user_permissions.add(dashboard_access_perm)
        return user

    class Meta:
        model = User
        fields = existing_user_fields(
            ['first_name', 'last_name', 'email']) + ['password1', 'password2']


class PartnerAddressForm(forms.ModelForm):
    name = forms.CharField(
        required=False, max_length=128,
        label=pgettext_lazy(u"Partner's name", u"Name"))
    is_active = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label=_('Is Active?'), 
                                  initial=False, widget=forms.Select, required=True)

    def __init__(self, *args, **kwargs):
        super(PartnerAddressForm, self).__init__(*args, **kwargs)
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

    class Meta:
        fields = ('name', 'is_active', 'full_address', 'sub_districts', 'city',
                  'state', 'postcode', 'country',)
        model = PartnerAddress