# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0006_auto_20150702_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='document_ptr',
        ),
        migrations.DeleteModel(
            name='Resume',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='version',
            new_name='options',
        ),
    ]
