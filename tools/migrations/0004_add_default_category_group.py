# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def add_default_category_group(apps, schema_editor):
    CategoryGroup = apps.get_model("tools", "CategoryGroup")
    obj, created = CategoryGroup.objects.get_or_create(
        name=settings.DEFAULT_CATEGORY_GROUP_NAME)


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_add_tool_perms_to_admins'),
    ]

    operations = [
        migrations.RunPython(add_default_category_group),
    ]
