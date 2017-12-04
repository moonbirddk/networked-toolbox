# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0015_auto_20171128_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGroupOverviewPage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.CharField(max_length=255, default='Lorem ipsum.')),
            ],
            options={
                'verbose_name': 'Category Group Overview Page',
            },
        ),
    ]
