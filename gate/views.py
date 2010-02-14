import os 
import simplejson

from gate.models import *
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response


def api(request):

    try:
        device_id = request.GET['device_id']
        pin = int(request.GET['pin'][:3])
        
        if device_id == '' or pin == 0:
            raise Execption('Device and pin must be provided')
        
        key = Key.objects.get(device_id=device_id, pin=pin, user__active=True)
        Access.objects.create(key=key, method=Access.METHOD_API, agent=request.META['HTTP_USER_AGENT'])
        
        if request.GET.has_key('test'):
            test = True
        else:
            
            #
            # here's where you trigger the door
            #
            
            test = False
        
        if request.GET.has_key('format') and request.GET['format'] == 'json':
            content = simplejson.dumps({'first_name':key.user.first_name, 'last_name':key.user.last_name, 'test':test})
            return HttpResponse(content, 'application/json')
        
        else:
            return render_to_response('txt/welcome.txt', {'name': key.user.first_name, 'test': test})
    
    except Exception, e:
        
        try:
            device_id = request.GET['device_id']
        except:
            device_id = ''
            
        try:
            pin = int(request.GET['pin'])
        except:
            pin = None
            
        FailedAccessAttempt.objects.create(device_id=device_id, pin=pin, method=Access.METHOD_API, agent=request.META['HTTP_USER_AGENT'])
        
        return HttpResponseForbidden()


def twilio(request):
  
    try:
        phone_number = request.POST['Caller']
        
        key = Key.objects.get(phone_number=phone_number, user__active=True)
        
        if request.POST.has_key('Digits'):
            
            pin = int(request.POST['Digits'][:3])
            
            if phone_number == '' or pin == 0:
                raise Execption('Phone nubmer and pin must be provided')
            
            if key.pin == pin:
                
                Access.objects.create(key=key, method=Access.METHOD_TWILIO, agent=request.META['HTTP_USER_AGENT'])
                #
                # here's where you trigger the door
                #
                
                return render_to_response('twilio/success.xml', {'name': key.user.first_name})
            else:
                FailedAccessAttempt.objects.create(phone_number=phone_number, pin=pin, method=Access.METHOD_TWILIO, agent=request.META['HTTP_USER_AGENT'])
                return render_to_response('twilio/failure.xml')
                
        else:
            return render_to_response('twilio/welcome.xml', {'name': key.user.first_name})
        
    except:
        try:
            phone_number = request.POST['Caller']
        except:
            phone_number = ''
            
        try:
            pin = int(request.GET['pin'])
        except:
            pin = None
            
        FailedAccessAttempt.objects.create(phone_number=phone_number, pin=pin, method=Access.METHOD_TWILIO, agent=request.META['HTTP_USER_AGENT'])
        return render_to_response('twilio/error.xml')
    

