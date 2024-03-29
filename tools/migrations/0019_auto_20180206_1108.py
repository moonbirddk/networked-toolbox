# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-06 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0018_auto_20180205_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='published',
            field=models.BooleanField(default=True, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='categories',
            field=models.ManyToManyField(related_name='tools', related_query_name='tool', to='tools.ToolCategory', verbose_name='toolboxes'),
        ),
    ]
