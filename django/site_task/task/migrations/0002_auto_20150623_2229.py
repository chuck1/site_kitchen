# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('desc', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='task',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='task',
            name='id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='taskbase_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='task.TaskBase'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_ep',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 22, 29, 22, 765171), verbose_name=b'date end planned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date_sp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 23, 22, 29, 22, 765136), verbose_name=b'date start planned'),
            preserve_default=True,
        ),
    ]
