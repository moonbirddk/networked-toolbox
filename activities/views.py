from django.shortcuts import render

def list_all(request):
    ctx = {
        'activities': [
            'Kræn Hansen commented on your story',
            'Someone used the same tool as you',
            'Kræn Hansen commented on your story',
        ]
    }
    return render(request, 'activities/list_all.html', ctx)
