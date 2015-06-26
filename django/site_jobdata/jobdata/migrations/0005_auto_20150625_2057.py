# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0004_auto_20150625_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
