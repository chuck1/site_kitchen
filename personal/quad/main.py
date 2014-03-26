import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

import math


import Quadcopter
import control
import quaternion as qt
from visual import *
import vec



dt = 0.01
N = 2000

t = np.arange(N) * dt


c = Quadcopter.Quad(t)
b = control.Brain(c)

#b.ctrl_position.fill_xref([1.0, 1.0, 0.0])

"""
b.objs = [
		control.Move([1.0,0.0,0.0],[0.01,0.01,0.01]),
		control.Move([1.0,1.0,0.0],[0.01,0.01,0.01]),
		control.Move([0.0,1.0,0.0],[0.01,0.01,0.01]),
		control.Move([0.0,0.0,0.0],[0.01,0.01,0.01]),
		control.Move([0.0,0.0,1.0],[0.01,0.01,0.01]),
		control.Move([1.0,0.0,1.0],[0.01,0.01,0.01]),
		control.Move([1.0,1.0,1.0],[0.01,0.01,0.01]),
		control.Move([0.0,1.0,1.0],[0.01,0.01,0.01]),
		control.Move([0.0,0.0,1.0],[0.01,0.01,0.01])]
"""
"""
b.objs = [
		control.Orient(qt.Quat(theta = math.pi, v = [1.0, 0.0, 0.0]), mode = control.ObjMode.hold)]
"""

b.objs = [
		control.Path(lambda t: np.array([math.sin(t * 4.0 / math.pi),t,0.0]))]


for ti in range(1,N):
	
	if (ti % (N / 100)) == 0:
		print ti

	b.step(ti-1)
	c.step(ti)
	
	


c.plot()


b.ctrl_position.plot()
b.ctrl_attitude.plot()


b.plot()

c.plot3()

pl.show()




