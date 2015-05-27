import math
import itertools

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, HttpResponseRedirect, HttpResponse
import django.db.models
import django.views.generic

from kitchen.models import *

import kitchen.graph
import kitchen.forms
import kitchen.funcs

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
        yield item, sum(a for i,a in gpr_list)

def recipeorder():
    grouped = itertools.groupby(gen_ings(), lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)
        yield item, sum(a for i,a in gpr_list)

# generator of (item, ir) tuples from transactions and recipe orders
def ir_list():
    objects = sorted(
            itertools.chain(gen_ings(), gen_trans()),
            key = lambda o: o[0].id)
    
    grouped = itertools.groupby(objects, lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)    
        ir = sum(a for o,a in gpr_list)
        yield item, ir
   

def demand_list():
    
    for item, ir in ir_list():
        
        d = demand(ir)
        
        if d > 0:
            yield item, ir, d

def myceil(x, m):
    d = x/m
    r = d % 1.0
    y = (d - r + math.ceil(r)) * m
    print("myceil x",x,"m",m,"y",y)
    return y

def test_in(G, item, d, ir_dict):
    for rec, itm, dic in G.G.in_edges(item, data=True):
        ing = dic['object']
        
        a = -d / ing.amount_std
        
        a = myceil(a, rec.lcm)
        
        yield rec, a, rec.can_make(-d / ing.amount_std, ir_dict)


def shoppinglist():

    G = kitchen.graph.IngGraph()
    
    dlist = list(demand_list())
    
    ir_dict = dict((item, ir) for item, ir in ir_list())
    
    for item, ir, d in dlist:
        
        #in_e = G.G.in_edges(item, data=True)

        recs = list(test_in(G, item, d, ir_dict))
        
        yield item, d / item.unit.convert, item.unit, item.category, recs

class ItemList(django.views.generic.ListView):
    #model = Transaction
    
    def get_queryset(self):
        return Item.objects.all()

def inventory_view(request):

    context = {'agg': list(inventory())}
    
    return render(request, 'kitchen/inventory.html', context)
    
def shoppinglist_view(request):

    context = {'items': sorted(list(shoppinglist()), key = lambda x: x[3])}

    return render(request, 'kitchen/shoppinglist.html', context)

# create a new recipe
def create_recipe(request):
    
    #r = get_object_or_404(Recipe)

    try:
        name = request.POST['name']
    except KeyError:
        return render(request, 'kitchen/error.html', {'message':'create recipe: KeyError'})
    else:
        r = Recipe()
        r.name = name
        r.save()
        
        return render(request, 'kitchen/error.html', {'message':'create recipe: Success'})
        #return HttpResponse('/django/admin/')
        #return HttpResponseRedirect('/django/admin/')

def ingredient_create(request):
    
    #r = get_object_or_404(Recipe)

    try:
        recipe_id = request.POST['recipe_id']
        item_id   = request.POST['item_id']
        unit_id   = request.POST['unit']
        amount    = request.POST['amount']
    except KeyError:
        return render(request, 'kitchen/error.html', {'message':'create recipe: KeyError'})
    else:
        recipe = get_object_or_404(Recipe, pk=int(recipe_id))
        item   = get_object_or_404(Item,   pk=int(item_id))
        unit   = get_object_or_404(Unit,   pk=int(unit_id))
        
        i = Ingredient()
        
        i.recipe = recipe
        i.item = item
        i.unit = unit
        i.amount = amount

        i.save()

        return HttpResponseRedirect('/django/kitchen/')

def create_recipe_order(request, recipe_id):
    
    r = get_object_or_404(Recipe, pk=recipe_id)

    try:
        amount = request.POST['amount']
    except KeyError:
        return render(request, 'kitchen/shoppinglist.html', {'items':[]})
    else:
        ro = RecipeOrder()
        ro.recipe = r
        ro.amount = amount
        ro.save()

        return HttpResponseRedirect(reverse('kitchen:shoppinglist_view'))
    
def create_transaction(request, item_id):
    
    item = get_object_or_404(Item, pk=item_id)
    
    try:
        amount = request.POST['amount']
    except KeyError:
        return render(request, 'kitchen/shoppinglist.html', {'items':[]})
    else:
        t = Transaction()
        t.item = item
        t.amount = amount
	t.unit = item.unit
        t.save()

        return HttpResponseRedirect(reverse('kitchen:shoppinglist_view'))

def add_recipe(request):
    if request.method == 'POST':
        form = kitchen.forms.add_recipe(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/admin/')

    else:
        form = kitchen.forms.add_recipe()

    return render(request, 'kitchen/add_recipe.html', {'form':form})

def index(request):
    return render(request, 'kitchen/index.html', {})


def item_selector(request):

    # pass through
    pass_through = []
    for p in request.POST.items():
        if p[0][0:3] == 'ud_':
            pass_through.append(p)

    selections = []
    i = 0
    while 1:
        name = "selection_{}".format(i)
        try:
            s = request.POST[name]
        except KeyError:
            break
            #return render(request, 'kitchen/error.html', {'message':'item selector: KeyError'})
        else:
            selections.append(s)
            i += 1
    
    tree = kitchen.funcs.item_selector_tree(selections)

    context = {
            'level':len(selections),
            'selections':zip(range(len(selections)), selections),
            'pass_through': pass_through,#request.POST.items(),
            'extra': pass_through,#request.POST.items(),
            }
    
    if isinstance(tree, list):
        choices = tree
        context['action'] = 'kitchen:item_selector_test'
        temp = 'kitchen/item_selector_final_0.html'
    else:
        choices = tree.keys()
        temp = 'kitchen/item_selector.html'

    context['choices'] = choices

    return render(request, temp, context)

def item_selector_final(request):
 
    # pass through
    pass_through = []
    for p in request.POST.items():
        if p[0][0:3] == 'ud_':
            pass_through.append(p)
   
    name = request.POST['name']

    action = request.POST['ud_action']

    cat = Category.objects.get(name=name)

    items = Item.objects.filter(category2=cat)

    context = {
            'choices': items,
            'action': action, #'kitchen:item_selector_test',
            'pass_through': pass_through,
    }
    
    temp = 'kitchen/item_selector_final_1.html'

    return render(request, temp, context)
  

def item_selector_test(request):
    name = request.POST['name']

    return HttpResponse("you selected item: {}".format(name))

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'kitchen/recipe_list.html', {'recipes':recipes})

def recipe_edit(request, recipe_id):
    return render(request, 'kitchen/recipe_edit.html', {'recipe_id': recipe_id})

def ingredient_add(request):

    recipe_id = request.POST['ud_recipe_id']

    item_id = request.POST['item_id']

    form = kitchen.forms.ingredient_add(request.POST)

    context = {
            'form':      form,
            'recipe_id': recipe_id,
            'item_id':   item_id,
            }

    return render(request, 'kitchen/ingredient_add.html', context)




