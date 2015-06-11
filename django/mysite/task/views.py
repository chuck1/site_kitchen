from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import django.db.models
import django.views.generic

# Create your views here.

import datetime
import pytz

import task.models

def task_sorter(x,y):
    if x[0].date_ea:
        print "has ea"
        return -1

    return cmp(x[0].date_ep, y[0].date_ep)

def gen_tasks():

    tz0 = pytz.timezone('America/Los_Angeles')
    
    for t in task.models.Task.objects.all():
 
        sp = t.date_sp
        sa = t.date_sa
        ep = t.date_ep
        ea = t.date_ea
        
        print "tzinfo"
        print sp.tzinfo
        #print sa.tzinfo
        print ep.tzinfo

        now = datetime.datetime.now(pytz.utc)


        #if sp.tzinfo is None:
        #    sp.tzinfo = pytz.utc
        #    sa.tzinfo = pytz.utc
        #    ep.tzinfo = pytz.utc

        sp_str = sp.astimezone(tz0).strftime("%Y/%m/%d %H:%M:%S")
        sa_str = ""
        ep_str = ""
        ea_str = ""

        if ep:
            ep_str = ep.astimezone(tz0).strftime("%Y/%m/%d %H:%M:%S")

        if ea:
            ea_str = ea.astimezone(tz0).strftime("%Y/%m/%d %H:%M:%S")

        if sa:
            sa_str = sa.astimezone(tz0).strftime("%Y/%m/%d %H:%M:%S")

        dp = ""
        da = ""
        

        if sa:
            if ea:
                da = ea - sa
            else:
                da = now - sa

            da = da - datetime.timedelta(microseconds=da.microseconds)

        
        if ep:
            dp = ep - sp

        yield (t, sp_str, sa_str, ep_str, ea_str, dp, da)

def calendar():
    t = datetime.date.today()
    m = t.month
    d = datetime.date(t.year, m, 1)
    
    w = 0
    cal = [[""]*7]
    
    while d.month == m:
        wd = d.weekday()
        cal[w][wd] = d.day

        d = d + datetime.timedelta(days=1)
        
        if wd == 6:
            if d.month != m:
                break
            
            cal.append([""]*7)
            w = w + 1

    

    return cal

def tasklist_view(request):

    tasks = list(sorted(gen_tasks(), task_sorter))
    tasks = filter(lambda t: t[0].date_ea is None, tasks)

    context = {'tasks': tasks, 'cal': calendar()}

    return render(request, 'task/tasklist.html', context)

def start_now(request, task_id):
    
    t = get_object_or_404(task.models.Task, pk=task_id)
    
    t.date_sa = datetime.datetime.utcnow()
    t.save()
    
    return HttpResponseRedirect(reverse('task:tasklist_view'))

def end_now(request, task_id):
    
    t = get_object_or_404(task.models.Task, pk=task_id)
    
    t.date_ea = datetime.datetime.utcnow()
    t.save()
    
    return HttpResponseRedirect(reverse('task:tasklist_view'))

def index(request):
    return render(request, 'task/index.html', {})
    

