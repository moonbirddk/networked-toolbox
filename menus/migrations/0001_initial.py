# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('menu', models.CharField(default='footer-left', choices=[('footer-left', 'Footer left'), ('footer-center', 'Footer center'), ('footer-right', 'Footer right')], max_length=20)),
                ('link', models.URLField(blank=True)),
                ('page', models.ForeignKey(related_name='menu_items', null=True, to='pages.Page')),
            ],
        ),
    ]
