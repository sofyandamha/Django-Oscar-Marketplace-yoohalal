from oscar.apps.checkout import app
from apps.shipping.app import application as shipping_app

app.application = shipping_app