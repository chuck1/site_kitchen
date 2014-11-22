import itertools

from django.shortcuts import render
import django.db.models
import django.views.generic
from kitchen.models import *

# ir (inventory - recipe order)
# t target inventory
# b buying threshhold
def demand(ir, t=0, b=0):
    return 0 if ir > b else t - ir

def gen_trans():
    for trans in Transaction.objects.all():
        yield trans.item, trans.amount_std

def gen_ings():
    for ro in RecipeOrder.objects.all():
        for ing in Ingredient.objects.filter(recipe=ro.recipe):
            yield ing.item, -ing.amount_std * ro.amount

def inventory():

    grouped = itertools.groupby(gen_trans(), lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)
        #yield item, sum(a for i,a in gpr_list), list(a for i,a in gpr_list)
        yield item, sum(a for i,a in gpr_list)


def recipeorder():

    grouped = itertools.groupby(gen_ings(), lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)
        #yield item, sum(a for i,a in gpr_list), list(a for i,a in gpr_list)
        yield item, sum(a for i,a in gpr_list)


def shoppinglist():
    
    objects = sorted(itertools.chain(gen_ings(), gen_trans()))
    
    grouped = itertools.groupby(objects, lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)
        #yield item, sum(a for o,a in gpr_list), list(a for o,a in gpr_list)

        ir = sum(a for o,a in gpr_list)
        d = demand(ir)
        
        if d > 0:
            yield item, d


# Create your views here.

class ItemList(django.views.generic.ListView):
    #model = Transaction
    
    def get_queryset(self):
        return Item.objects.all()

def inventory_view(request):

    context = {'agg': list(inventory())}
    
    return render(request, 'kitchen/inventory.html', context)
    
def shoppinglist_view(request):

    context = {'items': shoppinglist()}
    
    return render(request, 'kitchen/shoppinglist.html', context)

    
    


