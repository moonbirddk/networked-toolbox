# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(null=True, max_length=2),
        ),
    ]
