# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import migrations


def generate_uid(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    for profile in Profile.objects.all().iterator():
        if not profile.uid:
            profile.uid = uuid.uuid4().hex
            profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_profile_uid'),
    ]

    operations = [
        migrations.RunPython(
            generate_uid,
        ),
    ]
