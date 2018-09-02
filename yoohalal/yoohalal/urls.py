"""yoohalal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views

from oscar.app import application

from apps.banktransfer.dashboard.app import application as bank_dashboard
from apps.confirmation.dashboard.app import application as confirm_dashboard
from apps.slider.dashboard.app import application as slide_dashboard
from apps.blog.dashboard.app import application as blog_dashboard
from apps.subscribe.dashboard.app import application as subs_dashboard
from apps.career.dashboard.app import application as car_dashboard
from apps.confirmation.app import application as confirm
from apps.subscribe.app import application as subsc
from apps.career.app import application as careers
from apps.partner.app import application as partn
from apps.blog.app import application as blog
from apps.social_media.dashboard.app import application as sosmed
from apps.sitemaps import base_sitemaps

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^dashboard/bank-transfer/', include(bank_dashboard.urls)),
    url(r'^dashboard/confirmation/', include(confirm_dashboard.urls)),
    url(r'^dashboard/slider/', include(slide_dashboard.urls)),
    url(r'^dashboard/social_media/', include(sosmed.urls)),
    url(r'^dashboard/newsletter/', include(subs_dashboard.urls)),
    url(r'^dashboard/careers/', include(car_dashboard.urls)),
    url(r'^dashboard/blog/', include(blog_dashboard.urls)),
    url(r'^blog/', include(blog.urls)),
    url(r'^confirmation/', include(confirm.urls)),
    url(r'^newsletter/', include(subsc.urls)),
    url(r'^careers/', include(careers.urls)),
    url(r'^partner/', include(partn.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'', include(application.urls)),
    url(r'^sitemap\.xml$', views.index,
        {'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt', include('robots.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)