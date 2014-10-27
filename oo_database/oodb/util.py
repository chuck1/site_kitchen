import os
import pickle
import inspect

# get next available filename

def processRange(l):
        
        t = [None]*5
        b = [None]*5

        for r in l:
                for i in range(r.leftColumn(), r.rightColumn() + 1):
                        t1 = r.topRow()
                        b1 = r.bottomRow()
                        if not t[i] and not b[i]:
                                t[i] = t1
                                b[i] = b1
                                continue

                        if b1 >= (t[i] - 1) and b[i] >= (t1 - 1):
                                # overlap
                                t[i] = min(t[i], t1)
                                b[i] = max(b[i], b1)
                                continue

                        t[i] = None
                        b[i] = None
                        break

##                        print('b r', r.bottomRow())
##                        print('t r', r.topRow())
##                        print('l c', r.leftColumn())
##                        print('r c', r.rightColumn())
##                        ur += range(r.leftColumn(), r.rightColumn() + 1)

        #print('t b', t, b)

        t2 = None
        for t1 in t:
                if t1:
                        if t2:
                                t2 = max(t2, t1)
                        else:
                                t2 = t1

        b2 = None
        for b1 in b:
                if b1:
                        if b2:
                                b2 = min(b2, b1)
                        else:
                                b2 = b1
        
        if t2 and b2:
                if b2 >= t2:
                        rows = list(range(t2, b2 + 1))
                        cols = list(c for c in range(5) if t[c])
                        print('rows cols', rows, cols)
                        return rows, cols

        return None

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









