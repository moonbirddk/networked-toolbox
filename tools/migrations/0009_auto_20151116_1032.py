# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0008_add_admins_group_20151110_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolresource',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
