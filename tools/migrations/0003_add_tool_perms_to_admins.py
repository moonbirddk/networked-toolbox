# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
#from django.contrib.auth.models import Group, Permission
from django.db import migrations


def add_admins_group_with_perms(apps, schema_editor):
    Tool = apps.get_model("tools", "Tool")
    ToolCategory = apps.get_model("tools", "ToolCategory")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    admins, created = Group.objects.get_or_create(name='admins')
    tct = ContentType.objects.get_for_model(Tool)
    cct = ContentType.objects.get_for_model(ToolCategory)
    ct_ids = [tct.id, cct.id]
    for perm in Permission.objects.filter(content_type_id__in=ct_ids):
        if perm not in admins.permissions.all():
            admins.permissions.add(perm)
    admins.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('auth', '__latest__'),
        ('tools', '0002_new_site_domain'),
    ]

    operations = [
        migrations.RunPython(add_admins_group_with_perms),
    ]
