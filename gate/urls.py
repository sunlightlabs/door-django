from django.conf.urls import *


urlpatterns = patterns('gate.views',
      (r'^api/', 'api'),
      (r'^twilio/', 'twilio')
)