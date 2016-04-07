# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0005_auto_20160404_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('entry_type', model_utils.fields.StatusField(choices=[('favored', 'favored'), ('shared', 'shared'), ('commented', 'commented'), ('replied', 'replied')], no_check_for_status=True, max_length=100, default='favored')),
                ('title', models.CharField(max_length=150)),
                ('content', models.CharField(max_length=500)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
