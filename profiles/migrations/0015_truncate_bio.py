# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


TRUNCATE_BIO_SQL = '''UPDATE profiles_profile SET bio=substr(bio, 0, 401);'''


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20160512_1315'),
    ]

    operations = [
        migrations.RunSQL(TRUNCATE_BIO_SQL)
    ]
