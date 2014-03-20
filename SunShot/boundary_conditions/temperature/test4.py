
#import time
#import numpy as np
#import itertools
#from pylab import plot, show, figure, contour
#import pylab as pl
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#from sympy import *
#import math
#import inspect

#spreader_test()

from solver import *

n = 20

k = 10.0
alpha = 1.0
alpha_src = 1.0

x = [[0., 1.], [0., 1.], [0., 1.]]
n = [[10],[10],[10]]

prob = Problem('test4', k, alpha, alpha_src, it_max_1 = 1000, it_max_2 = 1000 )

p0 = prob.createPatch(1,	[1,	[0,1],	[0,1]],	x, n)
p1 = prob.createPatch(2,	[[0,1],	1,	[0,1]],	x, n)
p2 = prob.createPatch(3,	[[0,1],	[0,1],	1],	x, n)

stitch(p0,p1)
stitch(p1,p2)
stitch(p0,p2)

f0 = p0.faces[0,0]

f0.T_bou[0,0] = 10.
f0.T_bou[1,0] = 10.


prob.solve2(1e-4, 1e-4, True)
#prob.solve(1e-4)

prob.plot()

pl.plot(f0.Tmean)

pl.show()




