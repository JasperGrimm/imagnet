__author__ = 'djakson'
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from views import OrderForm
urlpatterns = patterns('',
    url(r'^$', 'magnet.views.order', name='_order'),
    url(r'^create/$', 'magnet.views.create_order', name="create_order"),
    url(r'^validate/$', 'magnet.views.validate', name='order_form_validate'),
    url(r'^duplicate/$', 'magnet.views.duplicate', name='duplicate_magnet'),
    url(r'^delete/$', 'magnet.views.delete', name='delete_magnet'),
    url(r'^edit/$', 'magnet.views.edit', name='edit_magnet'),
    url(r'^export/$','magnet.views.export', name="order_admin_export"),
    url(r'^(?P<order_num>[\d\w]+)/$', 'magnet.views.order', name='get_order'),

)
