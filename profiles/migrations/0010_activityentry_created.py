# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_activityentry_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityentry',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 7, 18, 17, 38, 870287, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
