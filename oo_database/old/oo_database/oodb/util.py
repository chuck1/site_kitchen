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
        raise 0
    
    # add the new obbject
    lst.append(obj)

    # rewrite database
    rm_data_files()
    save_to_next(lst)




