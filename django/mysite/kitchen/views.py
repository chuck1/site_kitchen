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

class shoppinglist_data(object):
    def __init__(self, 

def shoppinglist():

    G = kitchen.graph.IngGraph()
    
    dlist = list(demand_list())
    
    ir_dict = dict((item, ir) for item, ir in ir_list())
    
    for item, ir, d in dlist:
        
        #in_e = G.G.in_edges(item, data=True)

        recipes = list(test_in(G, item, d, ir_dict))
        
        cat = kitchen.funcs.category_top_for(item.category)

        yield item, d / item.unit.convert, item.unit, cat, recipes

class ItemList(django.views.generic.ListView):
    #model = Transaction
    
    def get_queryset(self):
        return Item.objects.all()

def inventory_view(request):

    context = {'agg': list(inventory())}
    
    return render(request, 'kitchen/inventory.html', context)
    
def shoppinglist_view(request):

    try:
        store_id = request.POST['store_id']
    except:
        store_id = None
    
    context = {'items': sorted(list(shoppinglist(store_id)), key = lambda x: x[3].id)}
    
    return render(request, 'kitchen/shoppinglist.html', context)

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'kitchen/recipe_list.html', {'recipes':recipes})

def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=int(recipe_id))
    return render(request, 'kitchen/recipe_edit.html', {
        'recipe':      recipe,
        'ingredients': Ingredient.objects.filter(recipe=recipe),
        })

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
        
        #return render(request, 'kitchen/error.html', {'message':'create recipe: Success'})
        #return recipe_edit(request, r.id)
        #return HttpResponse('/django/admin/')
        return HttpResponseRedirect("/django/kitchen/{}/recipe_edit/".format(r.id))

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

        return HttpResponseRedirect("/django/kitchen/{}/recipe_edit/".format(recipe_id))

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

def item_selector_final(request):
 
    # pass through
    pass_through = []
    for p in request.POST.items():
        if p[0][0:3] == 'ud_':
            pass_through.append(p)
   
    cat_name = request.POST['cat']

    action = request.POST['ud_action']

    cat = kitchen.models.Category.objects.get(name=cat_name)

    items = Item.objects.filter(category=cat)

    context = {
            'choices': items,
            'action': action, #'kitchen:item_selector_test',
            'pass_through': pass_through,
    }
    
    temp = 'kitchen/item_selector_final_1.html'

    return render(request, temp, context)

def item_selector(request):

    # pass through
    pass_through = []
    for p in request.POST.items():
        if p[0][0:3] == 'ud_':
            pass_through.append(p)

    try:
        cat = request.POST['cat']
    except KeyError:
        cat = None
        #return render(request, 'kitchen/error.html', {'message':'item selector: KeyError'})
    
    #tree = kitchen.funcs.item_selector_tree(selections)

    tree = kitchen.funcs.item_selector_tree2(cat)
    
    context = {
            'cat': cat,
            'pass_through': pass_through,#request.POST.items(),
            'extra': pass_through,#request.POST.items(),
            }
    
    #if isinstance(tree, list):
    if not tree:

        return item_selector_final(request)


        if not cat:
            return render(request, 'kitchen/error.html', {'message':'item selector: no category'})

        choices = kitchen.funcs.category_get_items(cat)
        context['action'] = 'kitchen:item_selector_test'
        temp = 'kitchen/item_selector_final_0.html'
    else:
        choices = tree
        temp = 'kitchen/item_selector.html'

    context['choices'] = choices

    return render(request, temp, context)

  

def item_selector_test(request):
    name = request.POST['name']

    return HttpResponse("you selected item: {}".format(name))


def item_list(request):
    
    items = kitchen.funcs.item_list()

    context = {'items':items}
    
    return render(request, 'kitchen/item_list.html', context)

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



def tree(request):
    
    c_lst = Category.objects.all()

    cr_lst = CategoryRelation.objects.all()

    c_lst_0 = []

    for c in c_lst:
        if not category_is_child(c):
            c_lst_0.append((
                c,
                category_get_children(c),
                Item.objects.filter(category=c)
                ))

    context = {'c_lst_0': c_lst_0}

    return render(request, 'kitchen/tree.html', context)













