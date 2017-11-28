# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0007_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
