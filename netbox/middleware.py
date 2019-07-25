from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login

from django.conf import settings


class RedirectToTermsAndConditionsMiddleware(object):
    """
    Redirects user to accept terms and conditions view
    before he/she is allowed to browse the site.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):

        if not settings.DJANGO_ENV == 'staging':
            return

        if request.path.startswith(settings.MEDIA_URL_PATTERN) or\
                request.path.startswith(settings.STATIC_URL_PATTERN):
            return

        try:
            if bool(int(request.COOKIES.get('has_accepted_terms', '0'))):
                return
        except (TypeError, ValueError) as exc:
            pass

        terms_url = reverse('profiles:terms_and_conditions')
        if request.path.startswith(terms_url):
            return

        to = request.get_full_path()
        return redirect_to_login(
            to,
            login_url=terms_url,
            redirect_field_name=REDIRECT_FIELD_NAME
        )
