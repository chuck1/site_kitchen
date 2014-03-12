
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

"""
f0 = Face(1, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],10.0)
f1 = Face(2, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],20.0)
f2 = Face(3, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],30.0)
"""

f0 = Face(1, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],10.0)
#f1 = Face(1, [1.,0.],[2.,1.], 1., [n,n],[20.,20.],[20.,20.],20.0)
f2 = Face(1, [0.,1.],[1.,2.], 1., [n,n],[20.,20.],[20.,20.],30.0)


"""
f0.nbrsur[0] = f1
f0.nbrsur[1] = f2

f1.nbrsur[1] = f0
f1.nbrsur[0] = f2

f2.nbrsur[0] = f0
f2.nbrsur[1] = f1
"""
#f0.nbrsur[0] = f1
f0.nbrsur[1] = f2

#f1.nbrsll[0] = f0

f2.nbrsll[1] = f0



faces = [f0, f2]

prob = Problem(faces)



prob.solve2(1e-4, 1e-2)

prob.plot()

save_prob(prob, 'case1')





