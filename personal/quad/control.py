import numpy as np

from vec import *

class Control_Attitude:
	def __init__(self, c):
		self.c = c
	
		# parameters
		C1_11 = 1.0
		C1_22 = 1.0
		C1_33 = 1.0

		C2_11 = 1.0
		C2_22 = 1.0
		C2_33 = 1.0

		L1_11 = 0.0
		L1_22 = 0.0
		L1_33 = 0.0

		self.C1 = np.array([
				[C1_11,0,0],
				[0,C1_22,0],
				[0,0,C1_33]])
		
		self.C2 = np.array([
				[C2_11,0,0],
				[0,C2_22,0],
				[0,0,C2_33]])
		
		self.L1 = np.array([
				[L1_11,0,0],
				[0,L1_22,0],
				[0,0,L1_33]])
		
		# variables
		self.e1 = np.zeros((c.N,3))
		self.chi1 = np.zeros((c.N,3))

		self.e2 = np.zeros((c.N, 3))
			
		self.theta_ref = np.zeros((c.N,3))
		self.theta_refd = np.zeros((c.N,3))
		self.theta_refdd = np.zeros((c.N,3))

		self.omega_ref = np.zeros((c.N,3))
	def get_f2(self, e1, e2):
		return -np.dot(self.C2,e2) - e1
	def step(self, ti):
		# refernce values must be set before stpping
		dt = self.c.t[ti] - self.c.t[ti-1]
		
		# reference
		if ti > 0:
			self.theta_refd[ti] = (self.theta_refd[ti] - self.theta_refd[ti-1]) / dt
			
		if ti > 1:
			self.theta_refdd[ti] = (self.theta_refd[ti] - self.theta_refd[ti-1]) / dt
		
		# tracking error
		self.e1[ti] = self.theta_ref[ti] - self.c.theta[ti]
		
		self.e2[ti] = self.omega_ref[ti] - self.c.omega[ti]
		
		self.chi1[ti] = self.chi1[ti-1] + self.e1[ti] * dt
		
		ver = False
		if ver:
			print 'theta_ref',self.theta_ref[ti]
			print 'theta    ',self.c.theta[ti]
			print 'e1       ',self.e1[ti]
	def get_tau_rotor_body(self, ti):
		
		e1 = self.e1[ti]
		e2 = self.e2[ti]
		
		f2 = self.get_f2(e1,e2)
		
		chi1 = self.chi1[ti]
		
		C1 = self.C1
		L1 = self.L1
		theta_refdd = self.theta_refdd[ti]
		
		A5  = self.c.get_A5(ti)
		A5d = self.c.get_A5d(ti)
		A5inv = self.c.get_A5inv(ti)
		
		omega = self.c.omega[ti]
		
		temp = np.dot(np.dot(C1, A5), e2 - np.dot(C1,e1) - np.dot(L1,chi1))
		
		temp2 = -f2 + temp + theta_refdd + np.dot(L1,e1) - np.dot(A5d,omega)
			
		temp3 = np.cross(omega, np.dot(self.c.I, omega))
	
		temp4 = np.dot(np.dot(self.c.I, A5inv), temp2)
	
		tau_RB = temp4 + temp3

		ver = False
		if ver:		
			print 'A5    ',A5
			print 'A5inv ',A5inv
			print 'A5d   ',A5d

			print 'theta_refdd',theta_refdd
		
			print 'temp  ',temp
			print 'temp2 ',temp2
			print 'temp3 ',temp3
			print 'temp4 ',temp4
			print 'e1    ',e1
			print 'e2    ',e2
			print 'A5    ',A5
			print 'C1    ',C1
			print 'f2    ',f2
			print 'temp  ',temp
			print 'tau_RB',tau_RB
	
		if any(np.isnan(tau_RB)):
			raise ValueError('nan')
		
		return tau_RB

class Control_Position:
	def __init__(self, c):
		self.c = c
		
		C5_11 = 2.0
		C5_22 = 2.0
		C5_33 = 1.5
		C6_11 = 0.5
		C6_22 = 0.5
		C6_33 = 2.5
		L5_11 = 0.0
		L5_22 = 0.0
		L5_33 = 0.0
		

		self.C5 = np.array([
				[C5_11,0,0],
				[0,C5_22,0],
				[0,0,C5_33]])
		self.C6 = np.array([
				[C6_11,0,0],
				[0,C6_22,0],
				[0,0,C6_33]])
		self.L5 = np.array([
				[L5_11,0,0],
				[0,L5_22,0],
				[0,0,L5_33]])
		
		self.e5 = np.zeros((c.N, 3))
		self.e6 = np.zeros((c.N, 3))
		self.chi5 = np.zeros((c.N, 3))

		self.xref = np.zeros((c.N, 3))
		self.xrefd = np.zeros((c.N, 3))
		self.xrefdd = np.zeros((c.N, 3))

		self.vref = np.zeros((c.N, 3))

		self.f_R = np.zeros((c.N, 3))
		
	def fill_xref(self, x):
		for ti in range(np.size(self.xref,0)):
			self.xref[ti] = x
	def get_f6(self, e5, e6):
		return -np.dot(self.C6,e6) - e5
	def step(self, ti):
		dt = self.c.t[ti] - self.c.t[ti-1]
	
		# reference
		self.xrefd[ti] = (self.xref[ti] - self.xref[ti-1]) / dt
		
		if ti > 1:
			self.xrefdd[ti] = (self.xrefd[ti] - self.xrefd[ti-1]) / dt
			
		# tracking error
		self.e5[ti] = self.xref[ti] - self.c.x[ti]
		self.e6[ti] = self.vref[ti] - self.c.v[ti]
		self.chi5[ti] = self.chi5[ti-1] + self.e5[ti] * dt 
	def get_force_rotor(self, ti):
		e5 = self.e5[ti]
		e6 = self.e6[ti]
		chi5 = self.chi5[ti]
		
		f6 = self.get_f6(e5,e6)

		C5 = self.C5
		L5 = self.L5
		
		m = self.c.m
		g = self.c.gravity		

		f_D = self.c.get_force_drag(ti)

		xrefdd = self.xrefdd[ti]
		
		temp1 = np.dot(C5, e6 - np.dot(C5, e5) - np.dot(L5, chi5))
		
		temp2 = np.dot(L5, e5)
		
		f_R = m * (-f6 + temp1 + xrefdd + temp2 - g) - f_D
		
		self.f_R[ti] = f_R
		
			
		ver = True
		if ver:
			print 'f6   ' ,f6
			print 'temp1' ,temp1
			print 'xrefdd',xrefdd
			print 'temp2 ',temp2
			print 'g     ',g
			print 'f_D   ',f_D

		return f_R

		
		
		
		
class Brain:
	def __init__(self, c):
		self.c = c

		self.ctrl_position = Control_Position(c)
		self.ctrl_attitude = Control_Attitude(c)
		
	def get_force_rotor_body(self, ti, f_R):
		
		# transform desired rotor force from inertial to body frame
		f_RB = np.dot(self.c.get_A6(ti), f_R)
		
		fz_RB = f_RB[2]
		
		return fz_RB
	def control_law_1(self, ti):
		gamma = np.zeros(4)
		
		return gamma
	def control_law_2(self, ti):
		# require position error
		self.ctrl_position.step(ti)
		
		f_R = self.ctrl_position.get_force_rotor(ti)
		
		
		
		theta = vec_to_euler(f_R/mag(f_R))
		
			
		# set attitude reference for previous step
		self.ctrl_attitude.theta_ref[ti] = theta
		
		# require attitude error
		self.ctrl_attitude.step(ti)
		
		tau_RB = self.ctrl_attitude.get_tau_rotor_body(ti)
		
		fz_RB = self.get_force_rotor_body(ti, f_R)
		
		
				
		gamma = np.dot(self.c.A4inv, np.append(tau_RB, fz_RB))
	
		ver = False
		if ver:
			print 'f_R',f_R
			print 'theta',theta
			print self.c.A4inv
			print tau_RB
			print np.append(tau_RB, fz_RB)
		

		return gamma
	def step(self, ti):
		
		
		gamma = self.control_law_2(ti)
		
		self.c.gamma[ti] = gamma
		
	def plot(self):
		#self.ctrl_x.plot()
		#self.ctrl_y.plot()
		#self.ctrl_z.plot()
		#self.ctrl_rot[0].plot()
		#self.ctrl_tilt.plot()
		pass

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

