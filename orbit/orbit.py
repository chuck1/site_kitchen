#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import numpy as np
import math
import sys

sys.path.append("/nfs/stak/students/r/rymalc/Documents/python")

import vector

def progress( value ):
	bar_length = 50
	
	block = int( round( bar_length * value ) )
	text = "\rprogress: [{0}]".format( "0"*block + "1"*(bar_length - block) )
	sys.stdout.write(text)
	sys.stdout.flush()


z_axis = np.array([0,0,1])


G = 6.674e-11

def fd1( y0, yp0, yp1, dx ):
	y1 = y0 + 0.5 * ( yp0 + yp1 ) * dx
	return y1

def fd0( y0, yp0, dx ):
	y1 = y0 + yp0 * dx
	return y1


def sphere( ax, r ):
	u = np.linspace(0, 2 * np.pi, 100)
	v = np.linspace(0, np.pi, 100)
	
	x = r * np.outer(np.cos(u), np.sin(v))
	y = r * np.outer(np.sin(u), np.sin(v))
	z = r * np.outer(np.ones(np.size(u)), np.cos(v))
	ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='g')



class sat:
	def init_abs( self, radius, mass, init_X ):
		self.radius = radius
		self.mass = mass
		self.mu = G * self.mass
		self.init_X = init_X
		self.init_V = np.zeros(3)
	def init_rel( self, parent, radius, alt, speed, init_lati, init_long, mass ):
		self.parent = parent
		self.alt = alt
		self.speed = speed
		self.init_lati = init_lati
		self.init_long = init_long
		self.mass = mass
		self.mu = G * self.mass

		init_x = math.cos(init_lati) * math.cos(init_long)
		init_y = math.cos(init_lati) * math.sin(init_long)
		init_z = math.sin(init_lati)
		
		
		init_uX = vector.norm( np.array([init_x,init_y,init_z]) )
		init_uV = vector.norm( np.cross( z_axis, init_uX ) )

		self.init_X = init_uX * ( alt + parent.radius )
		self.init_V = init_uV * speed

	def init_run( self, nt, dt ):
		self.x = np.zeros((nt,3))
		self.v = np.zeros((nt,3))
		self.f = np.zeros((nt,3))
		self.a = np.zeros((nt,3))
		self.V = np.zeros(nt)
		self.A = np.zeros(nt)
		self.c0 = np.zeros(nt)
				
		self.x[0,:] = np.array( self.init_X )
		self.v[0,:] = np.array( self.init_V )

		#self.stats(0)

	def stats( self, i ):
		self.V[i] = vector.magn( self.v[i,:] )
		self.A[i] = vector.magn( self.a[i,:] )
		self.c0[i] = self.A[i]/self.V[i]

		
	def step( self, dt, i ):
		v_old = np.array( self.v[i,:] )

		# acceleration
		self.a[i,:] = self.f[i,:] / self.mass

		# velocity
		self.v[i,:] = fd1( self.v[i-1,:], self.a[i-1,:], self.a[i,:], dt )
		
		#print self.a[i-1,:]	
		#print self.a[i,:]
		#print v_old
		#print self.v[i,:]
		
		#self.x[i,:] = fd0( self.x[i-1,:], self.v[i-1,:], dt )
		self.x[i,:] = fd1( self.x[i-1,:], self.v[i-1,:], self.v[i,:], dt )
		
		self.stats(i-1)
		
		V_delta = vector.magn( self.v[i,:] - v_old )
		V_old = vector.magn( v_old )
		
		#print "V_delta",V_delta,"V_old",V_old
		
		if V_old == 0:
			if V_delta == 0:
				return 0
			else:
				return 1
		else:
			return V_delta / V_old
		
		
	def plot_traj( self, ax ):
		ax.plot( self.x[:,0], self.x[:,1], self.x[:,2] )
	def plot_sphere( self, ax ):
		sphere( ax, self.radius )
	def plot_2dtraj( self, ax ):
		ax.plot( self.x[:,0], self.x[:,1] )

class system:
	def __init__( self, sats ):
		self.sats = sats
		self.nb_sats = len(sats)
		self.pairs = list( itertools.combinations( range(self.nb_sats), 2 ) )
		
	def run( self, nt, dt ):
		self.nt = nt
		self.dt = dt
		
		self.t = np.arange(0,nt) * dt

		for a in range(self.nb_sats):
			self.sats[a].init_run( nt, dt )

		self.accel(0)
		self.init_next_x(0)
		
		#print "starting loop"
		
		# loop
		for i in range(1,nt):
			progress(float(i)/float(nt))
			
			self.step(i)
		print
	
	def init_next_x( self, i ):
		if i < (self.nt-1):
			for s in self.sats:
				s.x[i+1] = np.array( s.x[i] )
				s.v[i+1] = np.array( s.v[i] )

	def accel( self, i ):
		# reset force
		for a in range(self.nb_sats):
			self.sats[a].f[i,:] = 0
		
		# calculate force
		for a in range(len( self.pairs )):
			b = self.pairs[a][0]
			c = self.pairs[a][1]
	
			r = self.sats[b].x[i,:] - self.sats[c].x[i,:]
			
			d = vector.magn( r )
			
			if d == 0:
				raise Exception("error: d=0")
			else:
				f = G * self.sats[b].mass * self.sats[c].mass / d / d * ( r / d )
			
			self.sats[b].f[i,:] -= f
			self.sats[c].f[i,:] += f
		
			
	def step( self, i ):
		self.init_next_x(i)
		
		while(1):
			self.accel(i)
			
			e = 0
			for a in range(self.nb_sats):
				e += self.sats[a].step( self.dt, i )
			
			#print "e",e
			
			if e < 0.0001:
				break

class orbit_elip:
	def v( self, r ):
		return math.sqrt( self.parent.mu * ( ( 2.0 / r ) - ( 1 / self.a ) ) )
	def __init__( self, parent, alt_a, alt_p ):
		self.parent = parent
		
		self.alt_p = alt_p
		self.alt_a = alt_a
		self.ra = alt_a + parent.radius
		self.rp = alt_p + parent.radius
		
		self.a = ( self.ra + self.rp ) / 2.0
		self.c = ( self.ra - self.rp ) / 2.0
		self.e = self.c / self.a
		
		self.va = self.v( self.ra )
		self.vp = self.v( self.rp )
		
		self.P = 2.0 * math.pi * math.sqrt( pow(self.a,3) / self.parent.mu )

	def theta( self, t ):
		return 2.0 * math.pi * t / self.P
class orbit_circ:
	def __init__( self, parent, alt ):
		self.parent = parent
		self.alt = alt
		
		self.r = self.alt + parent.radius
		
		self.v = math.sqrt( parent.mu / self.r )
		
		self.P = 2.0 * math.pi * math.sqrt( pow(self.r,3) / self.parent.mu )

	def theta( self, t ):
		return 2.0 * math.pi * t / self.P



def axis_equal_3d( ax ):
	w_lims = ax.get_w_lims()
	x_min = w_lims[0]
	x_max = w_lims[1]
	y_min = w_lims[2]
	y_max = w_lims[3]
	z_min = w_lims[4]
	z_max = w_lims[5]
	
	x_d = x_max - x_min
	y_d = y_max - y_min
	z_d = z_max - z_min
	
	w_min = min( [w_lims[0], w_lims[2], w_lims[4]] )
	w_max = max( [w_lims[1], w_lims[3], w_lims[5]] )
	w_d = w_max - w_min
	
	x_min -= ( w_d - x_d ) / 2.0
	x_max += ( w_d - x_d ) / 2.0
	y_min -= ( w_d - y_d ) / 2.0
	y_max += ( w_d - y_d ) / 2.0
	z_min -= ( w_d - z_d ) / 2.0
	z_max += ( w_d - z_d ) / 2.0
	
	ax.set_xlim3d( x_min, x_max )
	ax.set_ylim3d( y_min, y_max )
	ax.set_zlim3d( z_min, z_max )




