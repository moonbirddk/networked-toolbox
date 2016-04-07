# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_resources_perms(apps, schema_editor):
    ToolResource = apps.get_model("resources", "ToolResource")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    cgct = ContentType.objects.get_for_model(ToolResource)
    # db_alias = schema_editor.connection.alias

    if not Permission.objects.filter(codename='add_toolresource').exists():
        Permission.objects.create(
            codename='add_toolresource',
            name='Can add tool resource',
            content_type=cgct
        )

    if not Permission.objects.filter(codename='change_toolresource').exists():
        Permission.objects.create(
            codename='change_toolresource',
            name='Can change tool resource',
            content_type=cgct
        )

    if not Permission.objects.filter(codename='delete_toolresource').exists():
        Permission.objects.create(
            codename='delete_toolresource',
            name='Can delete tool resource',
            content_type=cgct
        )


def add_toolresource_perms_to_admins_group(apps, schema_editor):
    add_resources_perms(apps, schema_editor)
    ToolResource = apps.get_model("resources", "ToolResource")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    admins, created = Group.objects.get_or_create(name='admins')

    ContentType = apps.get_model("contenttypes", "ContentType")
    ct_tr = ContentType.objects.get_for_model(ToolResource)
    for perm in Permission.objects.filter(content_type_id=ct_tr.id):
        if perm not in admins.permissions.all():
            admins.permissions.add(perm)
    admins.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('auth', '__latest__'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_toolresource_perms_to_admins_group),
    ]
