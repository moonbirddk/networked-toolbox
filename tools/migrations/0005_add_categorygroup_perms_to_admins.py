# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_catgroup_perms(apps, schema_editor):
    CategoryGroup = apps.get_model("tools", "CategoryGroup")
    #Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    cgct = ContentType.objects.get_for_model(CategoryGroup)
    # db_alias = schema_editor.connection.alias

    if not Permission.objects.filter(codename='add_categorygroup').exists():
        Permission.objects.create(
            codename='add_categorygroup',
            name='Can add category group',
            content_type=cgct
        )

    if not Permission.objects.filter(codename='change_categorygroup').exists():
        Permission.objects.create(
            codename='change_categorygroup',
            name='Can change category group',
            content_type=cgct
        )

    if not Permission.objects.filter(codename='delete_categorygroup').exists():
        Permission.objects.create(
            codename='delete_categorygroup',
            name='Can delete category group',
            content_type=cgct
        )


def add_catgroup_perms_to_admins(apps, schema_editor):
    add_catgroup_perms(apps, schema_editor)
    CategoryGroup = apps.get_model("tools", "CategoryGroup")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    cgct = ContentType.objects.get_for_model(CategoryGroup)
    admins, created = Group.objects.get_or_create(name='admins')
    for perm in Permission.objects.filter(content_type_id=cgct.id):
        if perm not in admins.permissions.all():
            admins.permissions.add(perm)
    admins.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_add_default_category_group'),
    ]

    operations = [
        migrations.RunPython(add_catgroup_perms_to_admins),
    ]
