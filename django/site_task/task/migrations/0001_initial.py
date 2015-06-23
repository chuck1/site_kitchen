# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('desc', models.TextField(blank=True)),
                ('date_e', models.DateTimeField(auto_now_add=True, verbose_name=b'date entered')),
                ('date_sp', models.DateTimeField(default=datetime.datetime(2015, 6, 23, 3, 56, 14, 729067), verbose_name=b'date start planned')),
                ('date_sa', models.DateTimeField(null=True, verbose_name=b'date start actual', blank=True)),
                ('date_ep', models.DateTimeField(default=datetime.datetime(2015, 6, 24, 3, 56, 14, 729100), verbose_name=b'date end planned')),
                ('date_ea', models.DateTimeField(null=True, verbose_name=b'date end actual', blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'last modified')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
