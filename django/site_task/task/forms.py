import django.forms

import datetime

class task_add(django.forms.Form):
    title = django.forms.CharField(max_length=256)
    #desc = django.forms.TextField(blank=True)

    #date_e  = django.forms.DateTimeField(
    #        'date entered', auto_now_add = True)

    date_sp = django.forms.DateTimeField(
            'date start planned',)
            #default = datetime.datetime.now())

    date_sa = django.forms.DateTimeField(
            'date start actual')#, blank=True)#, null=True)

    date_ep = django.forms.DateTimeField(
            'date end planned',)
            #default = datetime.datetime.now() + datetime.timedelta(days=1))

    date_ea = django.forms.DateTimeField(
            'date end actual')#, blank=True)#, null=True)

    # repetition
    repeat = django.forms.BooleanField()
    
    repeat_mon = django.forms.BooleanField()
    repeat_tue = django.forms.BooleanField()
    repeat_wed = django.forms.BooleanField()
    repeat_thu = django.forms.BooleanField()
    repeat_fri = django.forms.BooleanField()
    repeat_sat = django.forms.BooleanField()
    repeat_sun = django.forms.BooleanField()
    
    choices = [
            ('never','never'),
            ('date','date'),
            ('occurances','occurances'),
            ]

    repeat_end_condition = django.forms.ChoiceField(choices=choices)






