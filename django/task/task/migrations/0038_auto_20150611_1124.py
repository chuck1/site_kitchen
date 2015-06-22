# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0037_auto_20150611_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_ep',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 12, 11, 24, 11, 563682), verbose_name=b'date end planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 11, 11, 24, 11, 563646), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
