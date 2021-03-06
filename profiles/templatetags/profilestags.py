from django import template
from ..utils import get_profile_photo_url

register = template.Library()


@register.inclusion_tag('profiles/_profile_photo.html')
def render_profile_photo(user, show_link=True):
    """
    {% render_profile_photo user %}
    """
    try: 
        photo_url = get_profile_photo_url(user)
    except: 
        return 
    
    if hasattr(user, "profile"): 
        return {
            'photo_url': photo_url,
            'profile_uuid': user.profile.uuid,
            'show_link': show_link,
            'title': user.profile.name,
            'user': user
        }


@register.inclusion_tag('profiles/_profile_photo.html')
def render_profile_photo_with_name(user, show_link=True, show_name=True):
    """
    {% render_profile_photo user %}
    """
    try: 
        photo_url = get_profile_photo_url(user)
    except: 
        return 
    if hasattr(user, "profile"): 
        return {
            'photo_url': photo_url,
            'profile_uuid': user.profile.uuid,
            'show_link': show_link,
            'show_name': show_name,
            'title': user.profile.name,
            'user': user
            }
    

@register.filter
def anim_delay(num, ad=0): 
    return '{}s'.format(num * 1.5 + 1.2 + ad)