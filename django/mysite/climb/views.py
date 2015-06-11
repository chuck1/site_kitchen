import django.shortcuts

# Create your views here.

import climb.forms
import climb.models

def index(request):
    return django.shortcuts.render(request, 'climb/index.html', {})

def route_create(request):
    if request.method == 'POST':
        form = climb.forms.route_create(request.POST)
        if form.is_valid():
            r = climb.models.Route()
            r.name     = form.cleaned_data['name']
            r.location = form.cleaned_data['location']
            r.area     = form.cleaned_data['area']
            r.wall     = form.cleaned_data['wall']
            r.save()

            return django.shortcuts.HttpResponseRedirect('/django/admin/climb/')
    else:
        form = climb.forms.route_create()

    return django.shortcuts.render(request, 'climb/route_create.html', {'form':form})




