import django

from django.conf.urls import url
from oscar.core.application import Application


class SocialMediaApplication(Application):
	name = 'link'

application = SocialMediaApplication()
