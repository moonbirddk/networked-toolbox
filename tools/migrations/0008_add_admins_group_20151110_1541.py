# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
#from django.contrib.auth.models import Group, Permission
from django.db import migrations


def add_tools_perms(apps, schema_editor):
    Tool = apps.get_model("tools", "Tool")
    ToolResource = apps.get_model("tools", "ToolResource")
    ToolCategory = apps.get_model("tools", "ToolCategory")
    #Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    tct = ContentType.objects.get_for_model(Tool)
    rct = ContentType.objects.get_for_model(ToolResource)
    cct = ContentType.objects.get_for_model(ToolCategory)
    db_alias = schema_editor.connection.alias

    Permission.objects.using(db_alias).bulk_create([
        Permission(codename='add_tool', name='Can add tool',
                   content_type=tct),
        Permission(codename='change_tool', name='Can change tool',
                   content_type=tct),
        Permission(codename='delete_tool', name='Can delete tool',
                   content_type=tct),
    ])
    Permission.objects.using(db_alias).bulk_create([
        Permission(codename='add_toolcategory',
                   name='Can add toolcategory',
                   content_type=cct),
        Permission(codename='change_toolcategory',
                   name='Can change toolcategory',
                   content_type=cct),
        Permission(codename='delete_toolcategory',
                   name='Can delete toolcategory',
                   content_type=cct),
    ])
    Permission.objects.using(db_alias).bulk_create([
        Permission(codename='add_toolresource',
                   name='Can add toolresource',
                   content_type=rct),
        Permission(codename='change_toolresource',
                   name='Can change toolresource',
                   content_type=rct),
        Permission(codename='delete_toolresource',
                   name='Can delete toolresource',
                   content_type=rct),
    ])


def add_admins_group_with_perms(apps, schema_editor):
    add_tools_perms(apps, schema_editor)
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    admins, created = Group.objects.get_or_create(name='admins')
    q = Q(
        Q(codename__endswith='_tool') |
        Q(codename__endswith='_toolcategory') |
        Q(codename__endswith='_toolresource')
    )
    for perm in Permission.objects.filter(q):
        admins.permissions.add(perm)
    admins.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('auth', '__latest__'),
        ('tools', '0007_datamigration_new_site_domain_20151110_1012'),
    ]

    operations = [
        migrations.RunPython(add_admins_group_with_perms),
    ]
