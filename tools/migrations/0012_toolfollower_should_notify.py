# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0011_auto_20151126_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolfollower',
            name='should_notify',
            field=models.BooleanField(default=False),
        ),
    ]
