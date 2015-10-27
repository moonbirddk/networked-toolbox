# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_tool_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='tools_images'),
        ),
    ]
