from datetime import datetime

from django.db import models

from django.contrib.auth.models import User


class DoorUser(models.Model):
    
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    class Meta:
        ordering = ['first_name']

class Key(models.Model):
    
    user = models.ForeignKey(DoorUser)
    
    description = models.CharField(max_length=255)
    
    phone_number = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    
    device_id = models.CharField(max_length=255, blank=True)
    
    pin = models.IntegerField()
    
    def __unicode__(self):
        return '%s %s (%s)' % (self.user.first_name, self.user.last_name, self.description)
    
    
class Access(models.Model):
    
    date = models.DateTimeField(default=datetime.now)
    
    key = models.ForeignKey(Key)
    
    METHOD_TWILIO = 1
    METHOD_API = 2
    
    METHOD_CHOICES = ((METHOD_TWILIO, 'Twilio'),
                      (METHOD_API, 'API'))
    
    method = models.IntegerField(choices=METHOD_CHOICES)
    
    agent = models.TextField(blank=True)
    
    def __unicode__(self):
        return '%s: %s %s' % (self.date, self.key.user.first_name, self.key.user.last_name, )
    

class FailedAccessAttempt(models.Model):
    
    date = models.DateTimeField(default=datetime.now)
    
    phone_number = models.CharField(max_length=10, blank=True)
    
    device_id = models.CharField(max_length=255, blank=True)
    
    pin = models.IntegerField(null=True)
    
    METHOD_TWILIO = 1
    METHOD_API = 2
    
    METHOD_CHOICES = ((METHOD_TWILIO, 'Twilio'),
                      (METHOD_API, 'API'))
    
    method = models.IntegerField(choices=METHOD_CHOICES)
    
    agent = models.TextField(blank=True)
    
    def __unicode__(self):
        
        if self.method == self.METHOD_API:
            return '%s (api): %s (%s)' % (self.date, self.device_id, self.pin)
        
        elif self.method == self.METHOD_TWILIO:
            return '%s (twilio): %s (%s)' % (self.date, self.device_id, self.pin)
    
    
    
    
    
    