# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection
from django.db import migrations


def update_sequence_on_categorygroup_id(apps, schema_editor):
    if 'postgresql' == connection.vendor:
        sql = """SELECT setval(pg_get_serial_sequence('"tools_categorygroup"',
        'id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM 
        "tools_categorygroup";"""
        migrations.RunSQL(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0005_add_categorygroup_perms_to_admins'),
    ]

    operations = [
        migrations.RunPython(update_sequence_on_categorygroup_id,
                             update_sequence_on_categorygroup_id),
    ]
