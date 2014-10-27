import os
import pickle
import inspect

# get next available filename

def next_file():
    m = 0

    for dirpath, dirnames, filenames in os.walk('data'):
        for filename in filenames:
            #print(filename)
            h,t = os.path.splitext(filename)

            i = int(h, 16)

            m = max(m,i)
    
    return m+1

def next_filename():
    return 'data/{0}.pkl'.format(next_file())

def save_to_next(l):
    
    f = open(next_filename(), 'wb')
    
    pickle.dump(l, f)
    
    f.close()

def get_next_id():
    with open('id.txt', 'r') as f:
        s = f.read()
    
    i = int(s)
    
    with open('id.txt', 'w') as f:
        f.write('{}'.format(i+1))

    return i

def reset_id():
    with open('id.txt', 'w') as f:
        f.write('0')

def get_data_filenames():
    for dirpath, dirnames, filenames in os.walk('data'):
        for filename in filenames:
            h,t = os.path.splitext(filename)
            if t == '.pkl':
                #print(filename)
                name = os.path.join(dirpath, filename)
                yield name

def rm_data_files():
    for name in get_data_filenames():
        os.remove(name)

def get_data():
    print('get data')
    l = []
    for name in get_data_filenames():
           
        with open(name, 'rb') as f:
            # a list of objects
            lst = pickle.load(f)

            l += lst

        #print(lst)

    for l in lst:
        l.resolve(lst)
    
    return l

def display(l, gen, attr_names):

    rows = []
    rows.append(attr_names)
    
    str = '{:32}'*len(attr_names)
    
    #print(str)
    #print(attr_names)
    #print(str.format(*attr_names))
    
    for s in gen(l):
        attr = []
        for an in attr_names:
            try:
                a = getattr(s, an)
            except:
                # attribute doesnt exist
                attr.append('None')
            else:
                if not a:
                    attr.append('None')
                else:
                    if inspect.ismethod(a):
                        #print('a is a method')
                        attr.append(a())
                    else:
                        attr.append(a)
            #print(an,":",a)
        #print(str.format(*attr))
        
        rows.append(list('{0}'.format(a) for a in attr))

    
    m = [0]*len(attr_names)
    for r in rows:
        for c in range(len(r)):
            m[c] = max(m[c], len(r[c])+1)


    str = ('{{:{}}}'*len(attr_names)).format(*m)
    
    
    for r in rows:
        print(str.format(*r))


def replace(obj, r):

    obj.id = r
    
    lst = get_data()
    
    found = False
    for i in range(len(lst)):
        if lst[i].id == r:
            found = True
            lst.pop(i)
            break
    
    if not found:
        raise Exception()
    
    # add the new obbject
    lst.append(obj)

    # rewrite database
    rm_data_files()
    save_to_next(lst)


def get_object(lst, i):
    found = False
    for o in lst:
        if o.id == r:
            found = True
            break
    
    if not found:
        raise Exception()
    
    return o

