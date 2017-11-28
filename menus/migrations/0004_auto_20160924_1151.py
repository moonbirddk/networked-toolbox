# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_auto_20160916_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='page',
            field=models.ForeignKey(null=True, related_name='menu_items', to='pages.Page', blank=True),
        ),
    ]
