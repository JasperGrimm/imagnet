from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = i18n_patterns('',
                            url(r'^admin/', include(admin.site.urls)),
                            url(r'^save/$', 'magnet.views.save', name='save_order'),
                            url(r'settings/$', include('dbsettings.urls')),
                            url(r'^payment/success/$', 'magnet.views.payment_success', name='payment_success'),
                            url(r'^payment/success/$', 'magnet.views.payment_fail', name='payment_fail'),
                            url(r'^payment/success/$', 'magnet.views.payment_result', name='payment_result'),
                            #url(r'^robokassa/', include('robokassa.urls')),
                            url(r'^', include('cms.urls')),
                            )

if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'', include('django.contrib.staticfiles.urls')),
                           ) + urlpatterns

