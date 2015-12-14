# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0019_auto_20151214_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='resources_text',
            field=models.CharField(default='Here you can find the different resources related to the current tool.', blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='toolcategory',
            name='resources_text',
            field=models.CharField(default='Here you can find the different resources related to the current category.', blank=True, max_length=300),
        ),
    ]
