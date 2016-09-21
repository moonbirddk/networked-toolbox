# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_menuitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.CharField(choices=[('footer-1', 'Networked Toolbox'), ('footer-2', 'The Network'), ('footer-3', 'The Toolbox')], max_length=20, default='footer-1'),
        ),
    ]
