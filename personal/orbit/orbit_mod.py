#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import itertools
import numpy as np
import math
import sys

sys.path.append("/nfs/stak/students/r/rymalc/Documents/python")

import vector



z_axis = np.array([0,0,1])


G = 6.674e-11

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
		self.init_X = init_X
		self.init_V = np.zeros(3)
	def init_rel( self, parent, radius, alt, speed, init_lati, init_long, mass ):
		self.parent = parent
		self.alt = alt
		self.speed = speed
		self.init_lati = init_lati
		self.init_long = init_long
		self.mass = mass
		
		init_x = math.cos(init_lati) * math.cos(init_long)
		init_y = math.cos(init_lati) * math.sin(init_long)
		init_z = math.sin(init_lati)
		
	
		init_uX = np.array([init_x,init_y,init_z])
		init_uV = vector.norm( np.cross(init_uX,z_axis) )

		self.init_X = init_uX * ( alt + parent.radius )
		self.init_V = init_uV * speed

	def init_run( self, nt, dt ):
		self.x = np.zeros((nt,3))
		self.v = np.zeros((nt,3))
		#self.r = np.zeros((nt,3))
		#self.d = np.zeros(nt)
		
		self.x[0,:] = self.init_X
		self.v[0,:] = self.init_V
		
		self.f = np.zeros((nt,3))
		
	def step( self, dt, i ):
		self.v[i] = self.v[i-1] + self.f[i] / self.mass * dt
		self.x[i] = self.x[i-1] + self.v[i] * dt
		
	def plot_traj( self, ax ):
		ax.plot( self.x[:,0], self.x[:,1], self.x[:,2] )
	def plot_sphere( self, ax ):
		sphere( ax, self.radius )
	def plot_2dtraj( self, ax ):
		ax.plot( self.x[:,0], self.x[:,1] )
	def orbit_expand( self, i, target_alt ):
		thrust = 1e5

		target_dist = target_alt + self.parent.radius

		target_speed = math.sqrt( G * self.parent.mass / ( target_dist ) )

		#print "speeds %e %e" % ( vector.magn( self.v[i-1,:] ),target_speed )
		
		target_pe = -G * self.parent.mass * self.mass / target_dist
		target_ke = 0.5 * self.mass * target_speed**2
		target_e = target_pe + target_ke

		rp = self.parent.x[i-1,:] - self.x[i-1,:]

		current_dist = vector.magn( rp )
		current_speed = vector.magn( self.v[i-1,:] )
		
		current_pe = -G * self.parent.mass * self.mass / current_dist
		current_ke = 0.5 * self.mass * current_speed**2
		current_e = current_pe + current_ke
						
		#print "distances %e %e" % ( current_dist, target_dist )
			
		print "energy %e %e" % ( current_e, target_e )
	
		if current_e < target_e:
		#if current_dist < target_dist:
			#f = vector.norm( rp ) * thrust
			f = vector.norm( self.v[i-1,:] ) * thrust
			print "burn"
			self.f[i] += f
	def init_anim( self, ax ):
		self.line, = ax.plot([],[],lw=2)
		self.line.set_data([],[])
		return self.line,
	def animate( self, i ):
		self.line.set_data( self.x[0:i,0], self.x[0:i,1] )
		return self.line,



def approach_control( r ):
	thrust = 1e5
	
	if vector.magn( r ) > 1.0e6:
		return  vector.norm( r ) * thrust
	else:
		return np.zeros(3)

class system:
	def __init__( self, sats ):
		self.sats = sats
		self.nb_sats = len(sats)
		self.pairs = list( itertools.combinations( range(self.nb_sats), 2 ) )
		
	def run( self, nt, dt ):
		self.nt = nt
		self.dt = dt
		
		t = np.arange(0,nt) * dt

		for a in range(self.nb_sats):
			self.sats[a].init_run( nt, dt )
	
		for i in range(1,nt):	
			self.step(i)
		
	def step( self, i ):
		
		for a in range(len( self.pairs )):
			b = self.pairs[a][0]
			c = self.pairs[a][1]
	
			r = self.sats[b].x[i-1,:] - self.sats[c].x[i-1,:]
			
			d = vector.magn( r )
			f = G * self.sats[b].mass * self.sats[c].mass / d / d * ( r / d )
			
			self.sats[b].f[i] -= f
			self.sats[c].f[i] += f

		# extra forces
		# ss to moon
		#rp = self.sats[1].x[i-1,:] - self.sats[1].parent.x[i-1,:]
		#tanj_p = 
		
		#self.sats[1].f[i] += approach_control( r )
		#self.sats[1].orbit_expand( i, 3.8e8 )
		
		

		for a in range(self.nb_sats):
			self.sats[a].step( self.dt, i )

	def init_anim( self, ax ):
		for s in self.sats:
			s.init_anim(ax)
	def animate( self, i ):
		for s in self.sats:
			s.animate(i)


class orbit_elip:
	def v( self, r ):
		return math.sqrt( G * self.parent.mass * ( 2.0 / r - 1 / self.a ) )
	def __init__( self, parent, alt_a, alt_p ):
		self.parent = parent
		self.ra = alt_a + parent.radius
		self.rp = alt_p + parent.radius
		
		self.a = ( self.ra + self.rp ) / 2.0
		self.c = ( self.ra - self.rp ) / 2.0
		self.e = self.c / self.a
		
		self.va = self.v( self.ra )
		self.vp = self.v( self.rp )



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




