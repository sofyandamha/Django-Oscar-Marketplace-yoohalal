from oscar.apps.checkout import app
from apps.banktransfer.app import application as checkout_app

app.application = checkout_app