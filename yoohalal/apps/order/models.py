from apps.address.abstract_models import (
    NewAbstractBillingAddress, NewAbstractShippingAddress)


class ShippingAddress(NewAbstractShippingAddress):
        pass

class BillingAddress(NewAbstractBillingAddress):
        pass

from oscar.apps.order.models import *  # noqa isort:skip
