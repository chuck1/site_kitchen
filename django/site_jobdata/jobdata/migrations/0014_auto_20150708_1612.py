# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jobdata.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0013_auto_20150707_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(null=True, upload_to=jobdata.models.upload_to_func, blank=True),
            preserve_default=True,
        ),
    ]
