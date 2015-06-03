
import kitchen.models

def category_is_child(c):
    cr_lst = kitchen.models.CategoryRelation.objects.all()

    for cr in cr_lst:
        if c == cr.child:
            return True

    return False

def category_get_children_list(c):
    cr_lst = kitchen.models.CategoryRelation.objects.all()

    ret = []

    for cr in cr_lst:
        if c == cr.parent:
            ret.append(cr.child)

    return ret


def category_get_children(c):
    cr_lst = kitchen.models.CategoryRelation.objects.all()

    ret = []

    for cr in cr_lst:
        if c == cr.parent:
            ret.append((
                cr.child,
                category_get_children(cr.child),
                kitchen.models.Item.objects.filter(category=cr.child)
                ))

    return ret

def category_top():
    c_lst = kitchen.models.Category.objects.all()

    ret = []

    for c in c_lst:
        if not category_is_child(c):
            ret.append(c)

    return ret

def category_top_for(c):
    if not category_is_child(c):
        return c
    
    cr_lst = kitchen.models.CategoryRelation.objects.filter(child=c)
    
    return category_top_for(cr_lst[0].parent)

def item_selector_tree2(cat_name):
    if not cat_name:
        return category_top()
    
    cat = kitchen.models.Category.objects.filter(name=cat_name)
    
    return category_get_children_list(cat[0])
     

def item_selector_tree(lst):

    branch_produce = {
                'monocots':{
                    'cepa':   ['white onion','red onion','sweet onion'],
                    'sativum':['garlic'],
                    },
                'eudicots':{
                    'asterids':{
                        'solanales':{
                            'annuum':      ['green bell pepper', 'red bell pepper'],
                            'lycopersicum':['tomato'],
                            },
                        'apiales':{
                            'carota':    ['carrot'],
                            'graveolens':['celery'],
                            },
                        },
                    'rosids':{
                        'malus':{
                            'domestica':['apple']
                            }
                        }
                    },
                }
    
    branch_meat = {
            'cow':    {},
            'pig':    {},
            'chicken':{},
            'fish':   {},
            }
    
    branch_cheese = {
            }

    branch_dairy = {
            }

    branch_bean = {
            }

    tree = {
            'produce':branch_produce,
            'meat':   branch_meat,
            'cheese': branch_cheese,
            'dairy':  branch_dairy,
            'bean':   branch_bean,
            'canned fruit': {},
            }
    
    t = tree

    for l in lst:
        t = t[l]
    
    return t

