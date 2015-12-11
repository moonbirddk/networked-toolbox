# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0015_remove_tool_field'),
    ]

    database_operations = [
        migrations.AlterModelTable('ToolResource', 'resources_toolresource')
    ]

    state_operations = [
        #migrations.DeleteModel('ToolResource')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations),
    ]
