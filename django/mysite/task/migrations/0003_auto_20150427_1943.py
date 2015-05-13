# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150427_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 19, 43, 47, 78241), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
