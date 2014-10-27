import pickle
import inspect

import oodb.classes
import oodb.class_util
import oodb.util

class DB:
    def __init__(self):
        
        self.lst = []
        for name in oodb.util.get_data_filenames():
               
            with open(name, 'rb') as f:
                # a list of objects
                lst = pickle.load(f)

                self.lst += lst
                
            #print(lst)

        for o in self.lst:
            o.resolve(self)

    def get_object(self, i):
        found = False
        for o in self.lst:
            if o.id == i:
                found = True
                break
        
        if not found:
            raise 0
        
        return o

    def display(self, gen, attr_names):

        rows = []
        rows.append(attr_names)
        
        str = '{:32}'*len(attr_names)
        
        #print(str)
        #print(attr_names)
        #print(str.format(*attr_names))
        
        for s in gen(self.lst):
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







