# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0003_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='file',
            field=models.FileField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
