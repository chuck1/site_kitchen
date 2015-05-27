def item_selector_tree(lst):
    tree = {
            'produce':{
                'monocots':{
                    'cepa':['white onion','red onion','sweet onion']
                    },
                'eudicots':{
                    'annuum':['green bell pepper', 'red bell pepper']
                    }
                },
            'meat':{}
            }
    
    t = tree

    for l in lst:
        t = t[l]
    
    return t

