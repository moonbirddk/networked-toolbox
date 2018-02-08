
from django.conf import settings


def homepage_display_results(request):
    limit = settings.HOMEPAGE_DISPLAY_RESULTS
    return {'HOMEPAGE_DISPLAY_RESULTS': limit}
