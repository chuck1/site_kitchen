import numpy as np
import math

from Quaternion import *

class Quad:
	def __init__(self, t):
		self.t = t
		self.gravity = np.array([0,0,-9.81])
		
		self.N = len(t)
		
		self.I = np.identity(3)
		self.Iinv = np.linalg.inv(self.I)
		
		self.m = 1.
		
		# state variables
		self.theta = np.zeros((self.N,3))
		self.omega = np.zeros((self.N,3))
		
		self.x = np.zeros((self.N,3))
		self.v = np.zeros((self.N,3))
		
		# constants
		self.L = 0.5
		
		self.k = 1.0
		self.b = 1.0

		# motor speed
		self.gamma = np.zeros((self.N,4))
		
		# matrices
		self.A1 = np.array([
				[self.L*self.k,		0,		-self.L*self.k,	0],
				[0,			self.L*self.k,	0,		-self.L*self.k],
				[self.b,		-self.b,	self.b,		-self.b]])		

		self.A2 = np.array([self.k,self.k,self.k,self.k,])
		
		self.A4 = np.append(self.A1, np.reshape(self.A2,(1,4)), 0)

		print self.A4
		self.A4inv = np.linalg.inv(self.A4)

		#print 'q',self.q._q
		#print 'w',self.w
	def get_S(self, ti):
		phi   = self.get_theta(ti)[0]
		theta = self.get_theta(ti)[1]
		
		st = math.sin(theta)
		ct = math.cos(theta)
		sp = math.sin(phi)
		cp = math.cos(phi)
		S = np.array([
				[1, 0, -st],
				[0, cp, ct * sp],
				[0, -sp, ct * cp]])
		return S
	def get_Sinv(self, ti):
		S = self.get_S(ti)
		Sinv = np.linalg.inv(S)
		return Sinv
	def get_R(self, ti):
		theta  = self.get_theta(ti)
		sp = math.sin(theta[0])
		st = math.sin(theta[1])
		ss = math.sin(theta[2])
		cp = math.cos(theta[0])
		ct = math.cos(theta[1])
		cs = math.cos(theta[2])
		R = np.array([
				[cp * cs - ct * sp * ss,	-cs * sp - cp * ct * ss,	st * ss],
				[ct * cs * sp + cp * ss,	cp * ct * cs - sp * ss,		-cs * st],
				[sp * st,			cp * st,			ct]])
		return R
	def get_A3(self, ti):
		q = self.q[ti]._q
		x = q[0]
		y = q[1]
		z = q[2]
		w = q[3]
		A3 = np.array([
			[-x,-y,-z],
			[ w,-z, y],
			[ z, w,-x],
			[-y, x, w]])
		return A3
	def get_thetap(self, ti):
		Sinv = self.get_Sinv(ti)
		omega = self.get_omega(ti)
		thetap = np.dot(Sinv, omega)
		return thetap
	def get_tau_body(self):
		tau = self.get_tau_rotor_body()
		return T
	def get_tau_rotor_body(self, ti):
		gamma = self.get_gamma(ti)
		tau = np.dot(self.A1, gamma)
		return tau	
	def force_rotor_body(self, ti):
		T = np.zeros(3)
		T[2] = np.dot(self.A2, self.get_gamma(ti))
		return T
	def get_force_drag_body(self, ti):
		return np.zeros(3)
	def get_force_drag(self, ti):
		return self.q[ti].rotate(self.get_force_drag_body(ti))
	def force(self, ti):
		F = self.gravity
		
		F = F + np.dot(self.get_R(ti), self.force_rotor_body(ti) + self.force_drag_body(ti))
		
		return F
		
	def position(self, ti):
		return np.reshape(self.x[ti,:],(3,))
	def velocity(self, ti):
		return np.reshape(self.v[ti,:],(3,))
	def get_omega(self, ti):
		return np.reshape(self.omega[ti,:],(3,))
	def get_theta(self, ti):
		return np.reshape(self.theta[ti,:],(3,))
	def get_gamma(self, ti):
		return np.reshape(self.gamma[ti,:],(4,))
	
	def step(self, ti):
		dt = self.t[ti] - self.t[ti-1]
		
		# rotation
		omega  = self.get_omega(ti-1)
		
		tau = self.get_tau_rotor_body(ti-1)
		
		omegap = np.dot(self.Iinv, tau - np.cross(omega, np.dot(self.I, omega)))
		
		theta  = self.get_theta(ti-1)
		thetap = self.get_thetap(ti-1)
		
		self.omega[ti] = omega + omegap * dt
		
		self.theta[ti] = theta + thetap * dt
		
		
		# position
		F = self.force(ti-1)
		v = self.velocity(ti-1)
		x = self.position(ti-1)
		
		a = F / self.m
		
		self.v[ti] = v + a * dt
		
		self.x[ti] = x + self.v[ti] * dt
		


		#print self.x



