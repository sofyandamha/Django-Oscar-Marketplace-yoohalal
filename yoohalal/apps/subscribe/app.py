from django.conf.urls import url
from oscar.core.application import Application
from . import views


class SubscribeApplication(Application):
    name = 'subscribe'

    def get_urls(self):
        urlpatterns = [
            url(r'^post/$', views.post_subscribe, name='post_subscribe'),
            url(r'^unsubscribe/(?P<ref>[-\w]+)/$', views.unsubscribe, name='unsubscribe'),
            url(r'^subscribe-form/$', views.SubscribeView.as_view(), 
                name='subscribe-form'),
            url(r'^thanks/(?P<ref>[-\w]+)/$', views.ThanksView.as_view(), 
                name='subscribe-thanks'),
        ]

        return self.post_process_urls(urlpatterns)


application = SubscribeApplication()
