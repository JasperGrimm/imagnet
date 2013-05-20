__author__ = 'djakson'
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'magnet.views.order', name='_order'),
    url(r'^create/$', 'magnet.views.create_order', name="create_order"),
    url(r'^(?P<order_num>[\d\w]+)/$', 'magnet.views.order', name='get_order'),
)
