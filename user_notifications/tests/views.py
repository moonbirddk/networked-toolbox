''' Django notifications views for tests '''
# -*- coding: utf-8 -*-
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user_notifications.signals import notify
from user_notifications.models import UserNotification

@login_required
def live_tester(request):
    notify.send(sender=request.user, recipient=request.user, verb='you loaded the page')
    user_notificatons = UserNotification.objects.filter(recipient=request.user) 

    return render(request, 'test_live.html', {
        'unread_count': user_notifications.unread().count(),
        'notifications': user_notifications.all()
    })


def make_notification(request):

    the_notification = random.choice([
        'reticulating splines',
        'cleaning the car',
        'jumping the shark',
        'testing the app',
        'attaching the plumbus',
    ])

    notify.send(sender=request.user, recipient=request.user,
                verb='you asked for a notification - you are ' + the_notification)
