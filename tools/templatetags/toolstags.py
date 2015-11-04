import os

from django import template

register = template.Library()


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
        css = 'film'
    elif extension in ('jpg', ''):
        css = 'picture-o'
    elif extension == 'mp3':
        css = 'file-audio-o'
    else:
        css = 'file-text-o'
    return 'fa-{}'.format(css)
