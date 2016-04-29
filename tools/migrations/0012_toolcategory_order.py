# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0011_auto_20160425_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolcategory',
            name='order',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
