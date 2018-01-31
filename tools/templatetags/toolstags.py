import os

from django import template
from ..models import Tool

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
        css = 'file-video-o'
    elif extension in ('jpg', 'png'):
        css = 'file-image-o'
    elif extension == 'mp3':
        css = 'file-audio-o'
    else:
        css = 'file-text-o'
    return 'fa-{}'.format(css)

@register.inclusion_tag('tools/_tool_miniphoto.html')
def render_tool_miniphoto(pk):
    """
    {% render_tool_miniphoto tool.pk %}
    """
    photo_url = Tool.objects.get(pk=pk).cover_image
    return {
        'photo_url': photo_url,
        'title': Tool.objects.get(pk=pk).title,
        }
