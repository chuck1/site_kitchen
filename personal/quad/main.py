import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

import math


from Quaternion import *
from Quadcopter import *
from control import *
from visual import *
import vec


e0 = np.array([1.,0.,0.])
e1 = np.array([0.,1.,0.])
e2 = np.array([0.,0.,1.])

g_mag = -9.81
g = e2 * g_mag



dt = 0.01
N = 1000

t = np.arange(N) * dt





c = Quad(t)
b = Brain(c)

#b.set_target([0.2,0.2,0.0])
b.set_target([0.0,0.0,0.0])
b.set_target_velocity([0.0,0.0,0.0])

c.v[0,0] = 1.0


for ti in range(1,N):
	
	if (ti % (N / 100)) == 0:
		print ti

	b.step(ti)
	c.step(ti)
	
	


plot_quad(c)

b.plot()

plot_quad_3(c)

pl.show()




