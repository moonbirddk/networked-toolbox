# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0016_move_resources_20151210_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolresource',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='ToolResource',
        ),
    ]
