# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0017_categorygroup_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorygroup',
            options={'verbose_name': 'Work Area', 'verbose_name_plural': 'Work Areas'},
        ),
        migrations.AlterModelOptions(
            name='categorygroupoverviewpage',
            options={'verbose_name': 'Work Area Overview Page'},
        ),
        migrations.AlterModelOptions(
            name='categoryoverviewpage',
            options={'verbose_name': 'Toolbox Overview Page'},
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={'ordering': ['title'], 'verbose_name': 'Tool', 'verbose_name_plural': 'Tools'},
        ),
        migrations.AlterModelOptions(
            name='toolcategory',
            options={'ordering': ['order', 'group'], 'verbose_name': 'Toolbox', 'verbose_name_plural': 'Toolboxes'},
        ),
        migrations.AlterModelOptions(
            name='toolfollower',
            options={'verbose_name': "'Tool Follower", 'verbose_name_plural': 'Tool Followers'},
        ),
        migrations.AddField(
            model_name='categorygroup',
            name='main_text',
            field=models.TextField(blank=True, null=True, default='Lorem ipsum.', max_length=5000),
        ),
    ]
