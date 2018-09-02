from django.template.loader import render_to_string
from django.conf import settings
from oscar.apps.shipping import methods
from oscar.apps.shipping.scales import Scale
from oscar.core import prices
from decimal import Decimal as D

class Reguler(methods.Base):
    code = 'reguler'
    name = 'Reguler'

    charge_per_item = settings.SHIPPING_REGULER_CHARGE

    description = render_to_string(
        'shipping/reguler.html', {'charge_per_item': charge_per_item})

    def calculate(self, basket):
        myround = lambda x: float(int(x)) if int(x) == x else float(int(x) + 1)
        s = Scale()
        weight = s.weigh_basket(basket) / 1000
        total = D(myround(weight)) * self.charge_per_item
        return prices.Price(
            currency=basket.currency,
            excl_tax=total,
            incl_tax=total)


class Express(methods.Base):
    code = 'express'
    name = 'Express'

    charge_per_item = settings.SHIPPING_EXPRESS_CHARGE
    
    description = render_to_string(
        'shipping/express.html', {'charge_per_item': charge_per_item})

    def calculate(self, basket):
        myround = lambda x: float(int(x)) if int(x) == x else float(int(x) + 1)
        s = Scale()
        weight = s.weigh_basket(basket) / 1000
        total = D(myround(weight)) * self.charge_per_item
        return prices.Price(
            currency=basket.currency,
            excl_tax=total,
            incl_tax=total)