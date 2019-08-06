import uuid
from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.urls import reverse

from django_countries.fields import CountryField

from common.utils import generate_upload_path


def do_upload_profile_photo(inst, filename):
    return generate_upload_path(inst, filename, dirname='profile_photos')




PROFILE_BIO_MAX_LEN = 400


class ProfileManager(models.Manager):

    def get_or_create(self, *args, **kwargs):
        with transaction.atomic():
            qs = self.get_queryset().filter(*args, **kwargs)
            if not qs.count():
                return self.create(*args, **kwargs), True
            return qs.first(), False


class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=do_upload_profile_photo,
                              blank=True, null=True)
    bio = models.TextField(
        max_length=PROFILE_BIO_MAX_LEN,
        blank=True,
        null=True
    )
    country = CountryField(blank_label='where did this take place?',
                           blank=True, null=True)

    objects = ProfileManager()

    def __str__(self): 
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    
    def name(self):
        user = self.user
        if user.first_name and user.last_name:
            return "{} {}".format(user.first_name, user.last_name)
        elif user.first_name:
            return user.first_name
        elif user.last_name:
            return user.last_name
        else:
            return "Noname Nosurname"

    def short_name(self):
        user = self.user
        if user.first_name and user.last_name:
            last_name = user.last_name[0] + '.'
            return "{} {}".format(user.first_name, last_name)
        elif user.first_name:
            return user.first_name
        else:
            return user.last_name

    def has_existing_photo(self):
        return self.photo and \
            default_storage.exists(self.photo.name)

    def get_absolute_url(self):
        return reverse('profiles:show', args=(self.uuid, ))


# @receiver(post_save, sender=User, dispatch_uid='profiles-create_user_profile')
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(pre_save, sender=Profile, dispatch_uid="profiles-on_profile_pre_save")
# def on_profile_pre_save(sender, instance, **kwargs):
#     try:
#         old = Profile.objects.get(uuid=instance.uuid)
#     except Profile.DoesNotExist:
#         return

#     if old.photo and old.photo.name and old.photo != instance.photo and\
#             default_storage.exists(old.photo.name):
#         default_storage.delete(old.photo.name)


# @receiver(post_delete, sender=Profile,
#           dispatch_uid="profiles-on_profile_post_delete")
# def on_profile_post_delete(sender, instance, **kwargs):
#     if instance.photo and instance.photo.name and\
#             default_storage.exists(instance.photo.name):
#         default_storage.delete(instance.photo.name)
