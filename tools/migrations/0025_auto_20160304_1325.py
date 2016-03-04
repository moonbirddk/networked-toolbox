# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

# this is a hack for the issue with tools_toolresource being moved
# to resources app
createtools_sql = '''
CREATE TABLE IF NOT EXISTS tools_toolresource (
  id varchar(1) NULL,
  content_type varchar(1) NULL
);
'''


class Migration(migrations.Migration):

    reversible = False

    dependencies = [
        ('tools', '0024_add_categorygroup_perms_to_admins'),
    ]

    operations = [
        migrations.RunSQL(createtools_sql),
        migrations.RemoveField(
            model_name='toolresource',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='ToolResource',
        ),
    ]
