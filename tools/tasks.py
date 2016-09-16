from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives

from .models import Suggestion


def send_suggestion(related_object_type=None, suggestion_id=None):
    suggestion = Suggestion.objects.get(id=suggestion_id)
    domain = Site.objects.get(id=settings.SITE_ID).domain
    ctx = {
        'related_object_type': related_object_type,
        'suggestion': suggestion,
        'title': "New suggestion",
        'BASE_URL': 'http://{}'.format(domain),
    }
    subject = 'New suggestion'
    html_msg = render_to_string('tools/email/suggestion.html', ctx)
    txt_msg = render_to_string('tools/email/suggestion.txt', ctx)
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = [settings.SITE_ADMIN_EMAIL, ]

    msg = EmailMultiAlternatives(subject, txt_msg, email_from, email_to)
    msg.attach_alternative(html_msg, "text/html")
    msg.send()
