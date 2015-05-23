# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0002_remove_item_category2'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category2',
            field=models.ForeignKey(to='kitchen.Category', null=True),
            preserve_default=True,
        ),
    ]
