import numpy as np
import pylab as pl

def plot_quad_3(c):
	fig = pl.figure()
	ax = fig.gca(projection='3d')
	
	x = c.x[:,0]
	y = c.x[:,1]
	z = c.x[:,2]
	
	s = (np.max(np.max(c.x)) - np.min(np.min(c.x))) / 2.0
	
	ax.plot(x,y,z,'o')
	
	rx = (np.max(x)+np.min(x))/2.0
	ry = (np.max(y)+np.min(y))/2.0
	rz = (np.max(z)+np.min(z))/2.0

	ax.set_xlim3d(rx-s,rx+s)
	ax.set_ylim3d(ry-s,ry+s)
	ax.set_zlim3d(rz-s,rz+s)
def plot_quad(c):
	plot_quad_x(c)
	plot_quad_v(c)
def plot_quad_x(c):
	fig = pl.figure()

	ax = fig.add_subplot(221)
	ax.set_ylabel('x')
	ax.plot(c.t,c.x[:,0])

	ax = fig.add_subplot(222)
	ax.set_ylabel('y')
	ax.plot(c.t,c.x[:,1])

	ax = fig.add_subplot(223)
	ax.set_ylabel('z')
	ax.plot(c.t,c.x[:,2])

	ax = fig.add_subplot(224)
	ax.set_ylabel('xy')
	ax.plot(c.x[:,0],c.x[:,1])
	
def plot_quad_v(c):
	fig = pl.figure()

	ax = fig.add_subplot(221)
	ax.set_ylabel('vx')
	ax.plot(c.t,c.v[:,0])

	ax = fig.add_subplot(222)
	ax.set_ylabel('vy')
	ax.plot(c.t,c.v[:,1])

	ax = fig.add_subplot(223)
	ax.set_ylabel('vz')
	ax.plot(c.t,c.v[:,2])










