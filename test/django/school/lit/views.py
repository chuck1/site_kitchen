from django.shortcuts import render
import django.http

import lit.models

# Create your views here.

def index(request):
    return django.http.HttpResponse(request, "Hello")

def bib(request):

    pubs = lit.models.Publication.objects.all()
    
    print(pubs)
    
    def process(pubs):
        for pub in pubs:
            s = pub.bib
            print(s)
            s = s.replace('\r\n', '</br>\r\n')
            s += '<br/>'
            print(s)
            yield s
    
    context = {
            'bibs': process(pubs)
            }

    return render(request, 'lit/bib.html', context)

