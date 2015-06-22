# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20150427_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_ea',
            field=models.DateTimeField(null=True, verbose_name=b'date end actual', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_ep',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 28, 21, 8, 35, 48065), verbose_name=b'date end planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sa',
            field=models.DateTimeField(null=True, verbose_name=b'date start actual', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 8, 35, 48031), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='desc',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
