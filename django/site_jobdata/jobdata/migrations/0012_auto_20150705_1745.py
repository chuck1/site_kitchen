# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0011_auto_20150704_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='options',
            field=models.TextField(max_length=256),
            preserve_default=True,
        ),
    ]
