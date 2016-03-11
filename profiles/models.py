from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from common.utils import generate_upload_path


def do_upload_profile_photo(inst, filename):
    return generate_upload_path(inst, filename, dirname='profile_photos')


class Profile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to=do_upload_profile_photo,
                              blank=True, null=True)

    def name(self):
        user = self.user
        if user.first_name and user.last_name:
            return "{} {}".format(user.first_name, user.last_name)
        elif user.first_name:
            return user.first_name
        elif user.last_name:
            return user.last_name
        else:
            return user.email

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


@receiver(post_save, sender=User, dispatch_uid='profiles-create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile, dispatch_uid="profiles-on_profile_pre_save")
def on_profile_pre_save(sender, instance, **kwargs):
    try:
        old = Profile.objects.get(id=instance.id)
    except Profile.DoesNotExist:
        return

    if old.photo and old.photo.name and old.photo != instance.photo and\
            default_storage.exists(old.photo.name):
        default_storage.delete(old.photo.name)


@receiver(post_delete, sender=Profile,
          dispatch_uid="profiles-on_profile_post_delete")
def on_profile_post_delete(sender, instance, **kwargs):
    if instance.photo and instance.photo.name and\
            default_storage.exists(instance.photo.name):
        default_storage.delete(instance.photo.name)
