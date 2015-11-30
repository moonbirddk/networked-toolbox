# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tools', '0010_suggestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolFollower',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('tool', models.ForeignKey(related_name='followers', to='tools.Tool')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='toolfollower',
            unique_together=set([('user', 'tool')]),
        ),
    ]
