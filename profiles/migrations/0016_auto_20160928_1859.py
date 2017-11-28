# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_truncate_bio'),
    ]

    database_operations = [
        migrations.AlterModelTable('ActivityEntry', 'activities_activityentry')
    ]

    state_operations = [
        migrations.DeleteModel('ActivityEntry')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
