import oodb.classes

def all(lst):
    for l in lst:
        yield l

def designs(lst):
    for l in lst:
        if isinstance(l, oodb.classes.Design):
            yield l

def simulations(lst):
    for l in lst:
        if isinstance(l, oodb.classes.Simulation):
            yield l





