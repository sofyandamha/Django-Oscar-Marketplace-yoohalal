from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.apps.partner.abstract_models import AbstractStockRecord

from .abstract_models import NewAbstractPartner, NewAbstractPartnerAddress


class Partner(NewAbstractPartner):
	pass

class PartnerAddress(NewAbstractPartnerAddress):
	pass

class StockRecord(AbstractStockRecord):
	old_price = models.DecimalField(
        _("Old Price"), decimal_places=2, max_digits=12,
        blank=True, null=True)


from oscar.apps.partner.models import *