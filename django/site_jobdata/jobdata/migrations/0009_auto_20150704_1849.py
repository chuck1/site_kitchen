# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0008_auto_20150704_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='filemodel_ptr',
        ),
        migrations.RemoveField(
            model_name='person',
            name='filemodel_ptr',
        ),
        migrations.DeleteModel(
            name='FileModel',
        ),
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
