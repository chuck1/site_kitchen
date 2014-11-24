import math
import pylab as pl
import numpy as np

Q = 0.1
L = 3.0
Lp = 1.8
R = 0.3125
r = 0.375/2.0

def x(b):
    return np.sqrt(L**2 + R**2 - 2 * L * R * np.cos(b))

def V(x):
    return math.pi * r**2 * (x - Lp + Q)




print(V(x(0.0)))

b = np.linspace(0, 2.0*math.pi, 100)

pl.plot(b, V(x(b)))
pl.show()

