# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobdata', '0005_auto_20150625_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=256)),
                ('file_html', models.FileField(null=True, upload_to=b'', blank=True)),
                ('file_pdf', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('company', models.ForeignKey(to='jobdata.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='jobdata.Document')),
                ('order', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=('jobdata.document',),
        ),
        migrations.AddField(
            model_name='document',
            name='person',
            field=models.ForeignKey(to='jobdata.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='position',
            field=models.ForeignKey(to='jobdata.Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='template',
            field=models.ForeignKey(to='jobdata.DocTemplate'),
            preserve_default=True,
        ),
    ]
