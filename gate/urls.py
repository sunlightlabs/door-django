from django.conf.urls.defaults import *


urlpatterns = patterns('gate.views',
      (r'^api/', 'api'),
      (r'^twilio/', 'twilio')
)