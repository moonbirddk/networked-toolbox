# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0018_auto_20171204_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='category_group',
            field=models.ForeignKey(blank=True, null=True, to='tools.CategoryGroup', related_name='stories'),
        ),
        migrations.AlterField(
            model_name='story',
            name='tool',
            field=models.ForeignKey(blank=True, null=True, to='tools.Tool', related_name='stories'),
        ),
    ]
