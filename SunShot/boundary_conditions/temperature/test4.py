
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

n = 10


f0 = Face(1, [[0.,1.],[0.,1.]], 1., [n,n],[[10.,10.],[10.,10.]],10.0)
f2 = Face(2, [[0.,1.],[0.,1.]], 1., [n,n],[[30.,30.],[30.,30.]],30.0)


f0.nbrs[0,1] = f2
f2.nbrs[1,1] = f0

faces = [f0, f2]

prob = Problem(faces,'test4')


prob.solve2(1e-4, 1e-2)
#prob.solve(1e-4)

prob.plot3()

#save_prob(prob, 'case1')

pl.show()



