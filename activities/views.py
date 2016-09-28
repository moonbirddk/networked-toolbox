from django.shortcuts import render
from .models import ActivityEntry

def list_all(request):
    activities = ActivityEntry.objects.order_by('-created')[:25]

    ctx = {
        'activities': activities
    }
    return render(request, 'activities/list_all.html', ctx)
