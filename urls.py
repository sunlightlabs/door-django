from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    (r'^/admin/', include(admin.site.urls)),)
    (r'^/', include('gate.urls')),
    (r'^iphone/', direct_to_template, {'template': 'iphone.html'})
    (r'^.*', direct_to_template, {'template': 'default.html'})
)
