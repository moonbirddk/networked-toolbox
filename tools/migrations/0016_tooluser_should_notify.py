# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-03 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0015_tool_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tooluser',
            name='should_notify',
            field=models.BooleanField(default=False),
        ),
    ]
