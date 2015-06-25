from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.forms.util import ErrorList

import jobdata.forms

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

    if request.method == 'POST':
        form = jobdata.forms.login(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponse("login success")
                else:
                    return HttpResponse("disabled account")
                    # Return a 'disabled account' error message
            else:
                return HttpResponse("invalid login")
                # Return an 'invalid login' error message.
    else:
         form = jobdata.forms.login()
    
    return render(request, 'jobdata/form_login.html', {'form':form})


def logout_view(request):
    logout(request)
    # Redirect to a success page



