from django.conf import settings
from urllib.parse import quote



def get_profile_url(user):
    return reverse('profiles:show', args=(user.profile.uuid,))


def get_profile_photo_url(user):
    photo_url = settings.STATIC_URL + 'profiles/images/defaultUser.svg'
    photo_url = quote(photo_url)
    if (user is not None and 
        not user.is_anonymous and 
        hasattr(user,"profile") and
            user.profile.photo is not None and user.profile.photo.url is not None):
        photo_url = user.profile.photo.url
    return photo_url
