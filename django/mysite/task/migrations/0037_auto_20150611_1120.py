# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0036_auto_20150611_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_ep',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 12, 11, 20, 51, 827495), verbose_name=b'date end planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 11, 11, 20, 51, 827459), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
