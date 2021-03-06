# Generated by Django 2.2.3 on 2019-07-25 21:35
from django.apps import apps
from django.db import migrations


class Migration(migrations.Migration):

    def make_unique_uuids(apps, schema_editor): 
        from uuid import uuid4
        Profile = apps.get_model('profiles', 'Profile')
        for profile in Profile.objects.all(): 
            profile.uuid = uuid4()
            profile.save()
        

    dependencies = [
        ('profiles', '0004_profile_uuid'),
    ]

    operations = [
        migrations.RunPython(make_unique_uuids)
    ]
