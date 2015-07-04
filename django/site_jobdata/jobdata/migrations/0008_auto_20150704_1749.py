# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0007_auto_20150703_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='document',
            name='file_html',
        ),
        migrations.RemoveField(
            model_name='document',
            name='file_pdf',
        ),
        migrations.RemoveField(
            model_name='document',
            name='id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='file',
        ),
        migrations.RemoveField(
            model_name='person',
            name='id',
        ),
        migrations.AddField(
            model_name='document',
            name='filemodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='jobdata.FileModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='filemodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='jobdata.FileModel'),
            preserve_default=False,
        ),
    ]
