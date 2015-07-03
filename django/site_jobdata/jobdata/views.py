from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import django.contrib.auth
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.util import ErrorList
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
import django.utils.datastructures
import django.core.files.base

import json

import jobdata.forms
import jobdata.html
import jobdata.myjson

def clean(s):
    s = s.replace('.','_')
    s = s.replace('@','_')
    return s

def form_signup(request):

    if request.method == 'POST':
        form = jobdata.forms.signup(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pw1 = form.cleaned_data['pw1']
            pw2 = form.cleaned_data['pw2']
    
            try:
                user = User.objects.create_user(
                    username,
                    email,
                    pw1)
            except:
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(u"username not unique")

                return render(request, 'jobdata/form_signup.html', {'form':form})
           
            return HttpResponse("signup success")
    else:
        form = jobdata.forms.signup()
    
    return render(request, 'jobdata/form_signup.html', {'form':form})

def form_login(request):
    print "views.form_login"

    redirect = request.POST['redirect']
    redirect_url = request.POST['redirect_url']

    if request.method == 'POST':
        form = jobdata.forms.login(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a redirect page.
                    return my_render(request, redirect, redirect_url, None)
                else:
                    return HttpResponse("disabled account")
                    # Return a 'disabled account' error message
            else:
                return HttpResponse("invalid login")
                # Return an 'invalid login' error message.
    else:
         form = jobdata.forms.login()
   
    c = {
            'redirect':redirect,
            'redirect_url':redirect_url,
            'form':form,
            }

    return render(request, 'jobdata/form_login.html', c)

def my_render(request, redirect, redirect_url, user):
    print "views.my_render", redirect

    if redirect == 'jobdata:json_editor':
        return json_editor(request)

    c = {
            'redirect':redirect,
            'redirect_url':redirect_url,
            }
    
    return render(request, redirect_url, c)

def logout(request):
    print "views.logout"
    
    django.contrib.auth.logout(request)
   
    # Redirect to a success page
    print request.user
    print request.user.is_authenticated()

    redirect     = request.POST['redirect']
    redirect_url = request.POST['redirect_url']
    
    c = {
            'redirect':redirect,
            'redirect_url':redirect_url,
            }
   
    return my_render(request, redirect, redirect_url, None)


def json_editor(request):
    print "views.json_editor"
 
    user = request.user

    # authenticate user
    r = auth_check(request, 'json_editor')
    if r is not None:
        return r

    person = jobdata.models.Person.objects.get(user=user)

    person.validate_json()

    try:
        j_str = request.POST['json']

        person.file_save(j_str)

    except django.utils.datastructures.MultiValueDictKeyError:

        j_str = person.file_read()

    c = {
            'json'        :j_str,
            'redirect'    :'jobdata:json_editor',
            'redirect_url':'jobdata/json_editor.html',
            }
    
    return render(request, 'jobdata/json_editor.html', c)

def auth_check(request, page):
    print "views.auth_check", page
    
    user = request.user
    if request.user.is_authenticated():
        return None

    print "auth failed"

    c = {
            'form':jobdata.forms.login(),
            'redirect':"jobdata:{}".format(page),
            'redirect_url':"jobdata/{}.html".format(page),
            }

    return render(request, "jobdata/form_login.html", c)

import python_resume



def json_render(request):
    print "views.json_render"
 
    user = request.user

    # authenticate user
    r = auth_check(request, 'json_render')
    if r is not None:
        return r

    person = jobdata.models.Person.objects.get(user=user)

    f = person.file
    
    if f:
        j = f.read()
    else:
        j = "{}"

    if request.method == 'POST':
        form = jobdata.forms.json_render(request.POST)
        if form.is_valid():
            version  = form.cleaned_data['version']

            g = python_resume.Generator(
                    version=version,
                    )

            g.load_json(j)
            g.filt(version)

            j = g.info
    else:
        form = jobdata.forms.json_render()

    c = {
            'form':form,
            'json':j,
            'redirect':'jobdata:json_render',
            'redirect_url':'jobdata/json_render.html',
            }
    
    return render(request, 'jobdata/json_render.html', c)

def document_render(request, document_id):
    print "views.resume_render", request.method

    user = request.user
    
    # authenticate user
    r = auth_check(request, 'resume_render')
    if r is not None:
        return r

    person = jobdata.models.Person.objects.get(user=user)
    
    person.validate_json()
    
    j = person.file_read()
    
    # generate json selector
    json_html = jobdata.html.json_to_html(json.loads(j))
    
    # get form data
    if request.method == 'POST':
        form = jobdata.forms.resume_render(request.POST)
        if form.is_valid():
            #company  = form.cleaned_data['company']
            position = form.cleaned_data['position']
            #version  = form.cleaned_data['version']
            #order    = form.cleaned_data['order']
            options  = form.cleaned_data['options']

            options_json = json.loads(options)

            #print "company",  repr(company)
            print "position", repr(position)
            #print "version",  repr(version)

            if company:
                version = version+",company"
            else:
                version = version+",nocompany"

            # use python_resume
            g = python_resume.Generator(
                    version=version,
                    order=order)

            g.load_json(j)
            g.filt(version)

            html = g.render_text(name="resume_content",fmt="html")
        else:
            html = ""
    else:
        form = jobdata.forms.resume_render()
    
        html = ""
    
    
    c = {
            'json_html':json_html,
            'form': form,
            'html': html,
            }

    return render(request, 'jobdata/resume_render.html', c)

def document_list(request):
    
    documents = jobdata.models.Document.objects.all()
    
    c = {'documents':documents}

    return render(request, 'jobdata/document_list.html')
    

