from sympy import *

o0,o1,o2 = symbols('o0:3')
o0d,o1d,o2d = symbols('o0:3d')

f2,f2d,f2dd = symbols('f2,f2d,f2dd')


o = Matrix([o0,o1,o2])
od = Matrix([o0d,o1d,o2d])

f = Matrix([0,0,f2])
fd = Matrix([0,0,f2d])
fdd = Matrix([0,0,f2dd])


pprint(o)
pprint(fd)


c = fd + f.cross(o)

pprint(c)

d = fdd + 2 * fd.cross(o) + f.cross(od) + (f.cross(o)).cross(o)

pprint(d)

