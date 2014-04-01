
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


k = 10.0
alpha = 1.3
alpha_src = 1.0

n = 10

x = [[0., 1.], [0., 1.], [0., 1.]]
n = [[n+0],[n+2],[n+4]]

prob = Problem('test4', x, n, k, alpha, alpha_src,
		it_max_1 = 1000,
		it_max_2 = 500)

#prob.get_3d_axes()
#sys.exit(0)

p0 = None
p1 = None
p2 = None
p3 = None
p4 = None
p5 = None

#p0 = prob.createPatch(1,	[1,	[0,1],	[0,1]])
#p1 = prob.createPatch(2,	[[0,1],	1,	[0,1]])
p2 = prob.createPatch(3,	[[0,1],	[0,1],	1])
p3 = prob.createPatch(-1,	[0,	[1,0],	[1,0]])
p4 = prob.createPatch(-2,	[[1,0],	0,	[1,0]])
p5 = prob.createPatch(-3,	[[1,0],	[1,0],	0])



stitch(p0,p1)
stitch(p0,p2)
stitch(p0,p4)
stitch(p0,p5)

stitch(p1,p2)
stitch(p1,p3)
stitch(p1,p5)

stitch(p2,p3)
stitch(p2,p4)

stitch(p3,p4)
stitch(p3,p5)

stitch(p4,p5)



#f0 = p0.faces[0,0]
#f1 = p1.faces[0,0]
f2 = p2.faces[0,0]
f3 = p3.faces[0,0]
f4 = p4.faces[0,0]
f5 = p5.faces[0,0]



#f0.T_bou[1,0] = 10.

#f1.T_bou[0,0] = 10.

f2.T_bou[0,0] = 30.
f2.T_bou[1,0] = 30.

f3.T_bou[0,1] = 30.

f4.T_bou[0,0] = 10.

f5.T_bou[0,0] = 30.
f5.T_bou[1,0] = 30.



#prob.solve2(1e-2, 1e-4, True)
prob.solve(1e-4)

prob.plot3()

#pl.plot(f0.Tmean)

pl.show()




