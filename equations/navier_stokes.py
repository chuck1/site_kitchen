from sympy import *

t, P, n = symbols('t, P, n')

u = tensor.IndexedBase('u')
x = tensor.IndexedBase('x')

i, j = map(tensor.Idx, ['i', 'j'])

#expr = Derivative(u[i],t) + Derivative(u[i]*u[j], x[j]) + Derivative(P, x[i])



