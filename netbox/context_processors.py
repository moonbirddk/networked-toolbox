
from django.conf import settings


def timezone_name(request):
    tzstr = request.session.get('django_timezone', settings.TIME_ZONE)
    return {'TIMEZONE_NAME': tzstr}


def google_analytics_id(request):
    return {
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID
    }

def user_has_verified_email(request):
    if(request.user.is_authenticated):
        result = request.user.emailaddress_set.filter(verified=True).exists()
    else:
        result = False
    return {
        'user_has_verified_email': result
    }
