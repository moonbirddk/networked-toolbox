
from django import template
from ..utils import get_profile_photo_url

register = template.Library()


@register.inclusion_tag('profiles/_profile_photo.html')
def render_profile_photo(user, show_link=True):
    """
    {% render_profile_photo user %}
    """
    photo_url = get_profile_photo_url(user)
    return {
        'photo_url': photo_url,
        'profile_uid': user.profile.uid,
        'show_link': show_link, 
        'title': user.profile.name, 

        }
