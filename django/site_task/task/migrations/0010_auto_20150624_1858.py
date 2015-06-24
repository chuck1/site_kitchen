# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20150624_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='task',
            name='taskbase_ptr',
        ),
        migrations.DeleteModel(
            name='TaskBase',
        ),
        migrations.AddField(
            model_name='task',
            name='desc',
            field=models.TextField(default=None, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=None, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_ep',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 25, 18, 58, 20, 545451), verbose_name=b'date end planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 18, 58, 20, 545418), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
