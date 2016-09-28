# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0016_auto_20160928_1859'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='ActivityEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('entry_type', model_utils.fields.StatusField(no_check_for_status=True, choices=[('add_story', 'add_story'), ('add_comment', 'add_comment'), ('add_comment_reply', 'add_comment_reply')], max_length=100, default='add_story')),
                ('title', models.CharField(max_length=150)),
                ('content', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
