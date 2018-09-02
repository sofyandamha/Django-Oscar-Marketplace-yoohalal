from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from phonenumber_field.modelfields import PhoneNumberField

from oscar.core.compat import AUTH_USER_MODEL
from oscar.models.fields import AutoSlugField

from apps.address.abstract_models import NewAbstractAddress


@python_2_unicode_compatible
class NewAbstractPartner(models.Model):
    code = AutoSlugField(_("Code"), max_length=128, unique=True, populate_from='name')

    name = models.CharField(pgettext_lazy(u"Partner's name", u"Name"), max_length=128, blank=True)
    
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partner',
        null=True,
        verbose_name=_("User"))

    is_active = models.BooleanField(
        _("Is Active?"), default=False)

    @property
    def display_name(self):
        return self.name or self.code

    @property
    def primary_address(self):
        """
        Returns a partners primary address. Usually that will be the
        headquarters or similar.

        This is a rudimentary implementation that raises an error if there's
        more than one address. If you actually want to support multiple
        addresses, you will likely need to extend PartnerAddress to have some
        field or flag to base your decision on.
        """
        addresses = self.addresses.all()
        if len(addresses) == 0:  # intentionally using len() to save queries
            return None
        elif len(addresses) == 1:
            return addresses[0]
        else:
            raise NotImplementedError(
                "Oscar's default implementation of primary_address only "
                "supports one PartnerAddress.  You need to override the "
                "primary_address to look up the right address")

    def get_address_for_stockrecord(self, stockrecord):
        """
        Stock might be coming from different warehouses. Overriding this
        function allows selecting the correct PartnerAddress for the record.
        That can be useful when determining tax.
        """
        return self.primary_address

    class Meta:
        abstract = True
        app_label = 'partner'
        ordering = ('name', 'code')
        permissions = (('dashboard_access', 'Can access dashboard'), )
        verbose_name = _('Fulfillment partner')
        verbose_name_plural = _('Fulfillment partners')

    def __str__(self):
        return self.display_name


@python_2_unicode_compatible
class NewAbstractPartnerAddress(NewAbstractAddress):
    """
    A partner can have one or more addresses. This can be useful e.g. when
    determining US tax which depends on the origin of the shipment.
    """
    phone_number = PhoneNumberField(
        _("Phone number"), blank=True)
    
    partner = models.ForeignKey(
        'partner.Partner',
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('Partner'))

    class Meta:
        abstract = True
        app_label = 'partner'
        verbose_name = _("Partner address")
        verbose_name_plural = _("Partner addresses")