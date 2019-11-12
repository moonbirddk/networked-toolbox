from django.shortcuts import render
from django.http import JsonResponse
from .models import EventWorkshop
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
# Create your views here.

def list_events(request):
    
    queryset = EventWorkshop.objects.filter(published=True, start_datetime__gt=now()).order_by("start_datetime")
    print ("BLA")
    print (queryset)
    
    context = {
        'events': queryset,
        
    }
    return render(request, 'events_workshops/index.html', context)

def show_event(request, id):
    event = EventWorkshop.objects.get(id=id)
    context = {
        'event': event,
        'user': request.user, 
        'user_participates': request.user in event.participiants.all()
    }
    return render(request, 'events_workshops/see_event.html', context)

@login_required
@verified_email_required
def event_signup(request, id): 
    event = EventWorkshop.objects.get(id=id)
    event.participiants.add(request.user)
    event.save()
    subject = "You have signed up for en event on Reflection Action."
    message = """Dear {} {},
    We have signed you up for the event {}. 
    Thank you very much for your interest.
    
    Kind regards,
    Reflection Action""".format(
        request.user.first_name, 
        request.user.last_name, 
        event.title, 
    )
    request.user.email_user(
        subject, 
        message
    )
    return JsonResponse({
        'success': True
    })    

@login_required
@verified_email_required
def event_signoff(request, id): 
    event = EventWorkshop.objects.get(id=id)
    event.participiants.remove(request.user)
    event.save()
    subject = "You are no longer signed up for en event on Reflection Action."
    message = """Dear {} {},
    We have signed you off of the event {}.
    
    Kind regards,
    Reflection Action""".format(
        request.user.first_name, 
        request.user.last_name, 
        event.title, 
    )
    request.user.email_user(
        subject, 
        message
    )
 
    return JsonResponse({
        'success': True
    })    