# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0016_move_resources_20151210_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='resources_text',
            field=models.CharField(default='Here you can find the different resources related to the current tool.', max_length=300),
        ),
    ]
