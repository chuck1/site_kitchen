from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import django.db.models
import django.views.generic

# Create your views here.

import datetime

import task.models

def gen_tasks():
    for t in task.models.Task.objects.all():
        yield (
            t,
            t.date_sp.strftime("%Y/%m/%d %H:%M:%S"),
            t.date_sa.strftime("%Y/%m/%d %H:%M:%S"),
            t.date_ep.strftime("%Y/%m/%d %H:%M:%S"),
            )

    
def tasklist_view(request):

    context = {'tasks': list(gen_tasks())}

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


