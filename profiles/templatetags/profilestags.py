import os

import bleach
from django import template

register = template.Library()


@register.filter
def bleach_striptags(strval):
    return bleach.clean(strval, tags=[], strip=True, strip_comments=True)


