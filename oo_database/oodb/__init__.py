import pickle
import inspect
import numpy as np

import oodb.classes
import oodb.class_util
import oodb.util
import oodb.gui

from oodb.Database import Database

######

class Scival:
    def __init__(self, v, u):
        self.v = v
        self.u = u

#######

class ValueType:
    def __init__(self, editable = True):
        self.editable = editable

class Method(ValueType):
    def __init__(self, f):
        super(Method, self).__init__(False)
        self.f = f

    def prnt(self):
        return self.f()

class Value(ValueType):
    def __init__(self, obj, name, value, editable = True):

        self.name = name
        self.obj = obj

        if name in ['id']:
            editable = False
        
        super(Value, self).__init__(editable)
        
        self.data = value
        

    def prnt(self):
        return self.data

class Label(ValueType):
    def __init__(self, value):
        super(Label, self).__init__(False)
        self.data = value

    def prnt(self):
        return self.data

##########

def make_value(obj, name, value, editable = True):
    
    if inspect.ismethod(value):
        return Method(value)
    elif inspect.isfunction(value):
        return Method(value)
    else:
        return Value(obj, name, value, editable)






