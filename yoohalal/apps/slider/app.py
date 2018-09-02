import django
from django.conf.urls import url
from oscar.core.application import Application


class SliderApplication(Application):
	name = 'slider'

application = SliderApplication()
