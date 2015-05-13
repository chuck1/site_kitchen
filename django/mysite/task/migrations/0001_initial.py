# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('desc', models.TextField()),
                ('date_e', models.DateTimeField(auto_now_add=True, verbose_name=b'date entered')),
                ('date_sp', models.DateTimeField(verbose_name=b'date start planned')),
                ('date_sa', models.DateTimeField(verbose_name=b'date start actual')),
                ('date_ep', models.DateTimeField(verbose_name=b'date end planned')),
                ('date_ea', models.DateTimeField(verbose_name=b'date end actual')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
