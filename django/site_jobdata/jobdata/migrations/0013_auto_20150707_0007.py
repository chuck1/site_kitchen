# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0012_auto_20150705_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='position',
            field=models.ForeignKey(blank=True, to='jobdata.Position', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='template',
            field=models.ForeignKey(default=None, to='jobdata.DocTemplate'),
            preserve_default=False,
        ),
    ]
