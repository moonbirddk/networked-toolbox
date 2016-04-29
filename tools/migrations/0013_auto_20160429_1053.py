# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0012_toolcategory_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolcategory',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
