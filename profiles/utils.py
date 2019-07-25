from django.conf import settings
from urllib.parse import quote



def get_profile_url(user):
    return reverse('profiles:show', args=(user.profile.uid,))


def get_profile_photo_url(user):
    photo_url = settings.STATIC_URL + 'profiles/images/defaultUser.svg'
    photo_url = quote(photo_url)
    if user and not user.is_anonymous and user.profile and\
            user.profile.photo and user.profile.photo.url:
            #user.profile.has_existing_photo():
        photo_url = user.profile.photo.url
    return photo_url
