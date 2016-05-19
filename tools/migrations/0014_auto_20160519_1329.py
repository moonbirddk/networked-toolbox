# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0013_auto_20160429_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=models.TextField(max_length=5000),
        ),
    ]
