from django.shortcuts import render
from django.db.models import *
from django.views.generic import *
from kitchen.models import *

# Create your views here.

class TransactionList(ListView):
    #model = Transaction
    
    def get_queryset(self):
        return Transaction.objects.annotate(Sum('item'))

def inventory(request):
    inv = Transaction.objects.annotate(Sum('amount'))
    context = {'inv':inv}
    return render(request, 'kitchen/inventory.html', context)
    



