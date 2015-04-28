# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 19, 43, 39, 185960, tzinfo=utc), verbose_name=b'last modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 19, 42, 57, 887476), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
