import os

import bleach
from django import template

register = template.Library()


@register.filter
def bleach_striptags(strval):
    return bleach.clean(strval, tags=[], strip=True, strip_comments=True)
    

@register.filter
def css_filefield(filefield):
    """
    Filter, takes Django FileField instance as an argument
    and returns css class string.
    """
    if not filefield:
        return ''

    extension = os.path.splitext(filefield.name)[1].lstrip('.')

    if extension == 'mp4':
        css = 'file-video-o'
    elif extension in ('jpg', 'png'):
        css = 'file-image-o'
    elif extension == 'mp3':
        css = 'file-audio-o'
    else:
        css = 'file-text-o'
    return 'fa-{}'.format(css)
