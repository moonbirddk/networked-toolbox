# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20160407_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityentry',
            name='link',
            field=models.CharField(max_length=100, default='/'),
            preserve_default=False,
        ),
    ]
