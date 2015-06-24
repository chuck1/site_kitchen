# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150623_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(related_name='child', to='task.TaskBase', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_ep',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 25, 18, 30, 8, 283070), verbose_name=b'date end planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 18, 30, 8, 283034), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
