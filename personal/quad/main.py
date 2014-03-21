import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from Quaternion import *
import math
import vec

e0 = np.array([1.,0.,0.])
e1 = np.array([0.,1.,0.])
e2 = np.array([0.,0.,1.])

g_mag = -9.81
g = e2 * g_mag



dt = 0.01
N = 10000

t = np.arange(N) * dt



def sign(x):
	return math.copysign(1.0,x)

def clamp(x,minx,maxx):
	if x > maxx:
		print 'max',maxx
		return maxx
	elif x < minx:
		print 'min',minx
		return minx
	else:
		return x

def clampz(x,v):
	return clamp(x,-v,v)

def mag(a):
	return np.linalg.norm(a)

def set_arb_comp(a,b):
	am = mag(a)
	ah = a / am

	bm = mag(b)
	bh = b / bm
	
	bm2 = am / np.dot(ah,bh)
	
	return bm2

class Rotor:
	def __init__(self, d, x):
		w = 0.025
		self.w = np.array([0.0,0.0,w])
		self.x = np.array(x)
		
		# properties
		# friction
		self.c1 = 0.1
		
		self.throt = 0.0
		
		# lift
		self.c2 = 100. * d
		
		self.T_full_mag = 100. 
		
		self.T_full = e2 * self.T_full_mag
		
	def set_torque(self, T):
		self.throt = clampz(T / self.T_full_mag, 1.0)
		
	def torque(self):
		t_air = -self.c1 * self.w
		t_mot = self.T_full * self.throt

		#print 'throt',self.throt

		return t_air + t_mot
	def force(self):
		f = self.c2 * self.w
		#print 'f',f
		#print 'w',self.w
		if any(np.isnan(self.w)):
			raise ValueError('nan')
		
		return f
	def torque_quad(self):
		T = np.zeros(3)
		#T += self.torque()
		T += np.cross(self.x, self.force())
		return  T
	def force_quad(self):
		return self.force()
		
	def step(self, dt):
		T = self.torque()
		self.w += T * dt
		#print 'w', self.w
		
class Quad:
	def __init__(self):
		self.I = np.identity(3)
		self.Iinv = np.linalg.inv(self.I)
		
		self.m = 1.
		
		# state variables
		self.q = Quat(([0,0,1],0))
		self.w = np.zeros(3)
		
		self.x = np.zeros((1,3))
		self.v = np.zeros((1,3))
		
		self.L = 0.5
		
		self.F_rot = np.zeros((1,3))
		
		# rotors
		self.rotors = [
				Rotor( 1.,e0 * self.L),
				Rotor( 1.,e0 * -self.L),
				Rotor(-1.,e1 * self.L),
				Rotor(-1.,e1 * -self.L)] 
		
		print 'Quadcopter initialized'
		
		#print 'q',self.q._q
		#print 'w',self.w
		
	def torque(self):
		T = np.zeros(3)
		
		for r in self.rotors:
			T += r.torque_quad()
		
		return T
		
	def force(self):
		F = g

		# rotor lift force
		F_rot = np.zeros(3)
		
		for r in self.rotors:
			F_rot += r.force_quad()
		
		# rotate to global
		
		#print 'q      ',self.q._q
		#print 'F_rot 1',F_rot
		F_rot = self.q.rotate(F_rot)
		#print 'F_rot 2',F_rot
		
		#print np.shape(self.F_rot)
		#print np.shape(F_rot)
		self.F_rot = np.append(self.F_rot,np.reshape(F_rot,(1,3)),0)

		return F + F_rot
		
	def position(self):
		return np.reshape(self.x[-1,:],(3,))
	def velocity(self):
		return np.reshape(self.v[-1,:],(3,))

	def step(self, ti):
		for r in self.rotors:
			r.step(dt)
		
		# rotation
		T = self.torque()

		#print np.shape(self.Iinv)
		#print np.shape(T)
		al = np.dot(self.Iinv, np.reshape(T,(3,)))
		
		self.w += al * dt
		
		w_mag = np.linalg.norm(self.w)
		#print 'w_mag',w_mag
		
		if w_mag != 0:
			w = Quat((self.w/w_mag,w_mag*dt))
			self.q = w * self.q
		
		if any(np.isnan(self.q._q)):
			raise ValueError('nan')

		# position
		F = self.force()
		a = F/self.m
		
		v = self.velocity()
		vnew = v + a * dt
		
		x = self.position()
		xnew = x + vnew * dt
		
		#if telem:
		self.v = np.append(self.v, np.reshape(vnew,(1,3)), 0)
		self.x = np.append(self.x, np.reshape(xnew,(1,3)), 0)

		#print self.x		
	def plot3(self):
		fig = pl.figure()
		ax = fig.gca(projection='3d')
		
		x = self.x[:,0]
		y = self.x[:,1]
		z = self.x[:,2]
		
		s = (np.max(np.max(self.x)) - np.min(np.min(self.x))) / 2.0
		
		ax.plot(x,y,z,'o')
		
		rx = (np.max(x)+np.min(x))/2.0
		ry = (np.max(y)+np.min(y))/2.0
		rz = (np.max(z)+np.min(z))/2.0

		ax.set_xlim3d(rx-s,rx+s)
		ax.set_ylim3d(ry-s,ry+s)
		ax.set_zlim3d(rz-s,rz+s)
	def plot(self):
		self.plot_x()
		self.plot_v()
	def plot_x(self):
		fig = pl.figure()

		ax = fig.add_subplot(221)
		ax.set_ylabel('x')
		ax.plot(t,c.x[:,0])

		ax = fig.add_subplot(222)
		ax.set_ylabel('y')
		ax.plot(t,c.x[:,1])

		ax = fig.add_subplot(223)
		ax.set_ylabel('z')
		ax.plot(t,c.x[:,2])

		ax = fig.add_subplot(224)
		ax.set_ylabel('xy')
		ax.plot(c.x[:,0],c.x[:,1])
		
	def plot_v(self):
		fig = pl.figure()

		ax = fig.add_subplot(221)
		ax.set_ylabel('vx')
		ax.plot(t,c.v[:,0])

		ax = fig.add_subplot(222)
		ax.set_ylabel('vy')
		ax.plot(t,c.v[:,1])

		ax = fig.add_subplot(223)
		ax.set_ylabel('vz')
		ax.plot(t,c.v[:,2])


class PID:
	def __init__(self,p,i,d):
		self.i = i
		self.p = p
		self.d = d
		self.x = []
		self.y = []
		self.integral = 0.
		self.e = []
		self.v = []
		self.f = []
	def step(self, x, dt):
		self.x.append(x)
		self.y.append(self.target)
		
		self.e.append(self.target - x)
		
		if len(self.e) > 1:
			self.v.append( (self.e[-2] - self.e[-1]) / dt )
		else:
			self.v.append(0)
		
		self.integral += self.e[-1] * dt
		
		f = (self.i * self.integral) + (self.p * self.e[-1]) - (self.d * self.v[-1])
		self.f.append(f)

		#print 'e v f'
		#print self.e[-1], self.v[-1], self.f[-1]

	def plot(self):
		fig = pl.figure()
		ax = fig.add_subplot(221)
		ax.plot(self.x)
		ax.plot(self.y)
		ax.set_ylabel('position')

		ax = fig.add_subplot(222)
		ax.plot(self.v)
		ax.set_ylabel('velocity')

		ax = fig.add_subplot(223)
		ax.plot(self.f)
		ax.set_ylabel('force')


class Brain:
	def __init__(self, c):
		self.c = c
		
		# position control
		p = 0.1
		d = 2.0
		
		self.ctrl_x = PID(p,0.0,d)
		self.ctrl_y = PID(p,0.0,d)
		
		self.ctrl_z = PID(2.0,0.5,2.5)
		
		
		# velocity control
		p = 1.0
		i = 0.0
		d = 2.0
		
		self.ctrl_vx = PID(p,i,d)
		self.ctrl_vy = PID(p,i,d)
		self.ctrl_vz = PID(p,i,d)

		self.ctrl_tilt = PID(2.0,0.0,2.0)
		self.ctrl_tilt.target = 0.0
		

		
		# rotor speed control
		p = 40.0
		
		self.ctrl_rot = [
				PID(p,0.0,0.05),
				PID(p,0.0,0.05),
				PID(p,0.0,0.05),
				PID(p,0.0,0.05)]
		
		self.up = None
		self.d_up = None

	def set_target(self,x):
		self.x_target = x
		self.ctrl_x.target = x[0]
		self.ctrl_y.target = x[1]
		self.ctrl_z.target = x[2]
	
	def set_target_velocity(self,v):
		self.ctrl_vx.target = v[0]
		self.ctrl_vy.target = v[1]
		self.ctrl_vz.target = v[2]

	def control_force_xy_plane(self, ti, dt):
		x = self.c.position()
		v = self.c.velocity()

		# step the controllers
		self.ctrl_vx.step(v[0], dt)
		self.ctrl_vy.step(v[1], dt)
		
		# step the controllers
		self.ctrl_z.step(x[2], dt)

		# combine forces
		F = np.zeros(3)
		F[0] = self.ctrl_vx.f[-1]
		F[1] = self.ctrl_vy.f[-1]

		F[2] = self.ctrl_z.f[-1]

		# account for gravity
		F -= self.c.m * g

		# divide among rotors
		F /= 4.0

		return F


	def control_force_velocity(self, ti, dt):
		v = self.c.velocity()

		# step the controllers
		self.ctrl_vx.step(v[0], dt)
		self.ctrl_vy.step(v[1], dt)
		self.ctrl_vz.step(v[2], dt)
		

		# combine forces
		F = np.zeros(3)
		F[0] = self.ctrl_vx.f[-1]
		F[1] = self.ctrl_vy.f[-1]
		F[2] = self.ctrl_vz.f[-1]
		
		
		# account for gravity
		F -= self.c.m * g
		
		# divide among rotors
		F /= 4.0
		
		return F
		
	def control_force_position(self, ti, dt):
		# position
		x = self.c.position()

		# step the controllers
		self.ctrl_x.step(x[0], dt)
		self.ctrl_y.step(x[1], dt)
		self.ctrl_z.step(x[2], dt)
		

		# combine forces
		F = np.zeros(3)
		F[0] = self.ctrl_x.f[-1]
		F[1] = self.ctrl_y.f[-1]
		F[2] = self.ctrl_z.f[-1]


		# account for gravity
		F -= self.c.m * g

		# divide among rotors
		F /= 4.0

		return F
	
	def step(self, ti):
	
		#F = self.control_force_velocity(ti, dt)
		F = self.control_force_xy_plane(ti, dt)

		# z-comp
		F_z = F[2] * e2

		# rotate F to copter coord
		F_zc = self.c.q.inv().rotate(F_z)
		F_c = self.c.q.inv().rotate(F)
		
		# rotation between copter z-axis and F_c
		if self.up is None:
			self.up = -np.cross(e2, F_c)
		

		#c, _, c_angle, d_up = vec.angle(e2, F_c, self.up)
		c, _, c_angle, d_up = vec.angle(e2, F_c, np.cross(e2, F_c))

		#print 'F',F
		
		# tilt limiter
		#c_angle = clampz(c_angle, math.pi/4.0)
		
		if self.d_up:
			if sign(self.d_up) != sign(d_up):
				print 'r flipped!'
				#print 'x      ',x
				print 'z_c    ',self.c.q.rotate(e2)
				print 'c_angle',c_angle

		self.d_up = d_up


		# mean rotor force

		# set to z-comp of desired force
		F_m1 = F_c[2]
		
		# or ensure that global z-force equals desired
		F_m2 = set_arb_comp(F_zc,e2)

		#print 'z-comp method ',F_m1
		#print 'match z method',F_m2
		F_m = F_m2

		if c == None:
			print 'no tilt'

			F_rotors = np.zeros(4) + F_c[2]
		else:
			# evaluate tilt controller
			self.ctrl_tilt.step(c_angle, dt)
			T_r = self.ctrl_tilt.f[-1]
			
			# angle between rotation and copter x-axis
			_,_,theta,_ = vec.angle(e0, c, e2)
			
			

			s = math.sin(theta)
			c = math.cos(theta)

			

			F_ac = T_r * s / 2.0 / self.c.L
			F_bd = -F_ac * c / s

			"""
			print 'theta',theta
			print 'c/s',c/s
			print 'F_ac',F_ac
			print 'F_bd',F_bd
			"""

			# target rotor force
			F_rotors = np.array([-F_ac, F_ac, -F_bd, F_bd]) + F_c[2]
		
		#print 'F_rotors',F_rotors
		
		for r,ctrl,F_rot in zip(self.c.rotors, self.ctrl_rot, F_rotors):
			# set target rotor speed
			w = F_rot / r.c2
			ctrl.target = w
			
			# step ctrlr
			w = r.w[2]
			ctrl.step(w, dt)
			
			# set rotor torque
			T = ctrl.f[-1]
			r.set_torque(T)

	def plot(self):
		#self.ctrl_x.plot()
		#self.ctrl_y.plot()
		#self.ctrl_z.plot()
		self.ctrl_rot[0].plot()
		self.ctrl_tilt.plot()

c = Quad()
b = Brain(c)

#b.set_target([0.2,0.2,0.0])
b.set_target([0.0,0.0,0.0])
b.set_target_velocity([0.0,0.0,0.0])

c.v[0,0] = 1.0


for ti in range(N-1):
	
	if (ti % (N / 10)) == 0:
		print ti
	
	c.step(ti)
	b.step(ti)
	
	

c.plot()

b.plot()

c.plot3()

pl.show()




