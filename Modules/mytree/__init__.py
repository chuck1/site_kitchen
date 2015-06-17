

def list2tree(lst):
    
    d = dict()
    
    target = None

    for lst in lsts:
        for l in lst:
            try:
                target = d[l]
            except:
                d[l] = dict()
                target = d[l]

    return d



