# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def del_old_ctontent_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    try:
        ContentType.objects.filter(app_label='tools',
            model='toolresource').delete()
    except Exception as exc:
        print("fail to delete tools toolresource content types: {}".format(exc))


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0015_remove_tool_field'),
    ]

    database_operations = [
        migrations.AlterModelTable('ToolResource', 'resources_toolresource'),
        migrations.RunPython(del_old_ctontent_types),
    ]

    state_operations = [
        #this will be deleted in a later migration
        #migrations.DeleteModel('ToolResource')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations),

    ]
