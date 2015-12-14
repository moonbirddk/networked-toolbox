# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tools.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0022_add_default_category_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolcategory',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, to='tools.CategoryGroup', related_name='categories', default=tools.models.get_default_category_group_id, related_query_name='category'),
        ),
    ]
