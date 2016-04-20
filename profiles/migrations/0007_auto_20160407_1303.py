# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_activityentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityentry',
            name='entry_type',
            field=model_utils.fields.StatusField(max_length=100, default='add_story', choices=[(0, 'dummy')], no_check_for_status=True),
        ),
    ]
