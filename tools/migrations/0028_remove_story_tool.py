# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-09 14:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0027_auto_20180209_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='tool',
        ),
    ]
