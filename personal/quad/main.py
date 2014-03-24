import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

import math


from Quadcopter import *
from control import *
from visual import *
import vec



dt = 0.01
N = 1000

t = np.arange(N) * dt


c = Quad(t)
b = Brain(c)

b.ctrl_position.fill_xref([0.0, 0.0, 1.0])



for ti in range(1,N):
	
	if (ti % (N / 100)) == 0:
		print ti

	b.step(ti-1)
	c.step(ti)
	
	


plot_quad(c)

plot_ctrl_position(b.ctrl_position)

b.plot()

plot_quad_3(c)

pl.show()




