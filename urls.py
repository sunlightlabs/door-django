import settings
from django.conf.urls import *
from django.views.generic.simple import direct_to_template
from django.views.static import serve

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^/', include('gate.urls')),
    (r'iphone-media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
)

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root': settings.MEDIA_ROOT})
        )
    del(_media_url, serve)

urlpatterns += patterns('',
    (r'^iphone/', direct_to_template, {'template': 'iphone.html'}),
    (r'^.*', direct_to_template, {'template': 'default.html'}),
)