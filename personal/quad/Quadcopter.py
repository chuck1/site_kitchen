import numpy as np
import math

#Inverse[{{1,0,-sin(y)}, {0, cos(x), cos(y)*sin(x)}, {0, -sin(x), cos(y)*cos(x)}}]
#Inverse[{{1, 0, -Sin[y]}, {0, Cos[x], Cos[y] Sin[x]}, {0, -Sin[x], Cos[y] Cos[x]}}]

#{{0, Cos[f[t]] Tan[g[t]] f'[t] + Sec[g[t]]^2 Sin[f[t]] g'[t], -(Sin[f[t]] Tan[g[t]] f'[t]) + Cos[f[t]] Sec[g[t]]^2 g'[t]},
#{0, -(Sin[f[t]] f'[t]), -(Cos[f[t]] f'[t])},
#{0, Cos[f[t]] Sec[g[t]] f'[t] + Sec[g[t]] Sin[f[t]] Tan[g[t]] g'[t], -(Sec[g[t]] Sin[f[t]] f'[t]) + Cos[f[t]] Sec[g[t]] Tan[g[t]] g'[t]}}

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
	def get_A5(self, ti):
		return np.linalg.inv(self.get_A5inv(ti))
	def get_A5inv(self, ti):
		p = self.theta[ti,0]
		t = self.theta[ti,1]
		
		st = math.sin(t)
		ct = math.cos(t)
		sp = math.sin(p)
		cp = math.cos(p)
		
		A5inv = np.array([
				[1, 0, -st],
				[0, cp, ct * sp],
				[0, -sp, ct * cp]])
		return A5inv
	def get_A5d(self, ti):
		p = self.theta[ti,0]
		t = self.theta[ti,1]
		
		thetad = self.get_thetad(ti)
		
		pd = thetad[0]
		td = thetad[1]
		
		st = math.sin(t)
		ct = math.cos(t)
		sp = math.sin(p)
		cp = math.cos(p)
		
		tant = math.tan(t)
		sect = 1.0 / ct
		
		A5d = np.array([
			[0,	cp * tant * pd + sect**2 * sp * td,		-sp * tant * pd + cp * sect**2 * td],
			[0,	-sp * pd,					-cp * pd],
			[0,	cp * sect * pd + sect * sp * tant * td,		-sect * sp * pd + cp * sect * tant * td]])
		
		return A5d
	def get_A6(self, ti):
		theta  = self.theta[ti]
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
	def get_thetad(self, ti):
		A5 = self.get_A5(ti)
		omega = self.omega[ti]
		thetap = np.dot(A5, omega)
		return thetap
	def get_tau_body(self):
		tau = self.get_tau_rotor_body()
		return T
	def get_tau_rotor_body(self, ti):
		gamma = self.gamma[ti]
		tau = np.dot(self.A1, gamma)
		return tau
	def get_force_rotor_body(self, ti):
		T = np.zeros(3)
		T[2] = np.dot(self.A2, self.gamma[ti])
		return T
	def get_force_drag_body(self, ti):
		return np.zeros(3)
	def get_force_drag(self, ti):
		return np.dot(self.get_A6(ti), self.get_force_drag_body(ti))
	def get_force(self, ti):
		f_g = self.gravity
		
		f_B = self.get_force_rotor_body(ti) + self.get_force_drag_body(ti)
		
		A6 = self.get_A6(ti)
		
		f = f_g + np.dot(A6, f_B)

		ver = False
		if ver:	
			print 'A6 ',A6
			print 'f_g',f_g
			print 'f_B',f_B
			print 'f  ',f
		
		return f
		
	
	def step(self, ti):
		dt = self.t[ti] - self.t[ti-1]
		
		# rotation
		omega  = self.omega[ti-1]
		
		tau = self.get_tau_rotor_body(ti-1)
		
		omegap = np.dot(self.Iinv, tau - np.cross(omega, np.dot(self.I, omega)))
		
		theta  = self.theta[ti-1]
		thetap = self.get_thetad(ti-1)
		
		self.omega[ti] = omega + omegap * dt
		
		self.theta[ti] = theta + thetap * dt
		
		
		# position
		F = self.get_force(ti-1)
		
		x = self.x[ti-1]
		v = self.v[ti-1]
		
		a = F / self.m
		
		
		self.v[ti] = v + a * dt
		
		self.x[ti] = x + self.v[ti] * dt
		


		#print self.x



