# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_activityentry_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='uid',
            field=models.CharField(editable=False, unique=True, null=True,
                                   max_length=32),
        ),
    ]
