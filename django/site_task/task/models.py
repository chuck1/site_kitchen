from django.db import models

# Create your models here.

import django.utils

import datetime
#import pytz

class Task(models.Model):
    title = models.CharField(max_length=256)
    desc = models.TextField(blank=True)

    date_e  = models.DateTimeField(
            'date entered', auto_now_add = True)

    date_sp = models.DateTimeField(
            'date start planned',
            default = datetime.datetime.now())

    date_sa = models.DateTimeField(
            'date start actual', blank=True, null=True)

    date_ep = models.DateTimeField(
            'date end planned',
            default = datetime.datetime.now() + datetime.timedelta(days=1))

    date_ea = models.DateTimeField(
            'date end actual', blank=True, null=True)
    
    last_modified = models.DateTimeField('last modified', auto_now = True)
    
    # repetition data
    parent = models.ForeignKey('Task', null=True)#Base, null=True, related_name="child")
    
    def __unicode__(self):
        return self.title



