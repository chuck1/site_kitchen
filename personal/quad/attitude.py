
import math
import pylab as pl
import numpy as np

class Attitude1:
	def __init__(self, c):
		self.c = c
	
		# parameters
		C1_11 = 5.2
		C1_22 = 5.2
		C1_33 = 5.2

		C2_11 = 24.0
		C2_22 = 24.0
		C2_33 = 24.0

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

		self.tau_RB = np.zeros((c.N,3))
	def set_q_reference(self, ti, q):
		self.theta[ti] = vec_to_euler(q.v / mag(q.v))
		
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
		self.chi1[ti] = self.chi1[ti-1] + self.e1[ti] * dt
		
		# step omega_ref before stepping e2
		self.omega_ref[ti] = np.dot(self.C1, self.e1[ti]) + self.theta_refd[ti] + np.dot(self.L1, self.chi1[ti])
		
		# step e2
		self.e2[ti] = self.omega_ref[ti] - self.c.omega[ti]
		
		
		
		ver = False
		if ver:
			print 'theta_ref',self.theta_ref[ti]
			print 'theta    ',self.c.theta[ti]
			print 'e1       ',self.e1[ti]
		
	def get_tau_rotor_body(self, ti):
		# require error values
		self.step(ti)
		
		
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

		ver = True
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
		
		self.tau_RB[ti] = tau_RB
		
		return tau_RB


class Attitude2:
	def __init__(self, c):
		self.c = c
		
		self.q_ref = np.empty(c.N, dtype=object)
	
		self.K_PH = 1.0
		self.K_Pz = 1.0
		
		self.K_D = np.array([
				1.0,
				1.0,
				1.0])

		self.tau_RB = np.zeros((c.N,3))

	def set_q_reference(self, ti, q):
		self.q_ref[ti] = q
		
	def get_tau_RB(self, ti):
		
		q = self.q_ref[ti]

		alpha_H = math.acos(1.0 - 2.0*(q.v[0]**2 + q.v[1]**2))
		psi = 2.0 * math.atan2(q.v[2],q.s)
		
		rx = (math.cos(psi/2.0) * q.v[0] - math.sin(psi/2.0) * q.v[1]) / math.sin(alpha_H/2.0)
		ry = (math.sin(psi/2.0) * q.v[0] + math.cos(psi/2.0) * q.v[1]) / math.sin(alpha_H/2.0)


		beta_H = math.atan2(ry,rx)
		gamma_H = math.atan2(rx,-ry)
		
		tau_PH = self.K_PH * alpha_H
		tau_Pz = self.K_Pz * psi
		
		tau_D = np.multiply(self.K_D, self.c.omega[ti])
		
		tau_RB = np.array([
				tau_PH * math.cos(beta_H),
				tau_PH * math.sin(beta_H),
				tau_Pz])
		
		tau_RB += tau_D
		
		self.tau_RB[ti] = tau_RB
		
		return tau_RB
		
	def plot(self):
		fig = pl.figure()
		
		ax = fig.add_subplot(111)
		ax.plot(self.c.t, self.tau_RB)
		ax.set_xlabel('t')
		ax.set_ylabel('tau_RB')

class Attitude3:
	def __init__(self, c):
		self.c = c
		
		self.q_ref = np.empty(c.N, dtype=object)
	
		C1 = 3.0
	
		self.C1 = np.array([
				[C1,0.0,0.0],
				[0.0,C1,0.0],
				[0.0,0.0,C1]])
		
		C2 = 2.0
		
		self.C2 = np.array([
				[C2,0.0,0.0],
				[0.0,C2,0.0],
				[0.0,0.0,C2]])
		
		self.e1 = np.empty(c.N, dtype=object)
		self.e2 = np.zeros((c.N,3))
		
		self.q_refd = np.zeros((c.N,3))
		self.omega_ref = np.zeros((c.N,3))
		
		self.tau_RB = np.zeros((c.N,3))

	def set_q_reference(self, ti, q):
		self.q_ref[ti] = q

	def step(self, ti, ti_0):
		dt = self.c.t[ti] - self.c.t[ti-1]
		
		q = self.c.q[ti]
		q_ref = self.q_ref[ti]
		
		self.e1[ti] = q_ref * q.conj()
		
		
		# q_refd
		if ti_0 > 1:
			r = self.q_ref[ti] * self.q_ref[ti-1].conj()
			q_refd_n = r.to_omega(dt)
			#print 'r',r.s,r.v
		else:
			q_refd_n = np.zeros(3)		
		
		self.q_refd[ti] = q_refd_n
		
		# omega ref
		self.omega_ref[ti] = self.q_refd[ti]
		
		# omega error
		self.e2[ti] = self.omega_ref[ti] - self.c.omega[ti]

		ver = False
		if ver:		
			print 'q_refd_n',q_refd_n
		
	def get_tau_RB(self, ti, ti_0):
		# require error values
		self.step(ti, ti_0)
		
		q_ref = self.q_ref[ti]
		
		q = self.c.q[ti]
		
		
		e1 = self.e1[ti]
		
		tau_RB = np.dot(self.C1, e1.v) + np.dot(self.C2, self.e2[ti])
		
		self.tau_RB[ti] = tau_RB
		
		if any(np.isnan(tau_RB)):
			print q_ref.s,q_ref.v
			print q.s,q.v
			print e1.s, e1.v
			
			
			raise ValueError('tau_RB nan')
		
		return tau_RB
		
	def plot(self):
		self.plot_q()
		self.plot_omega()
	def plot_q(self):
		fig = pl.figure()

		t = self.c.t
		
		ax = fig.add_subplot(111)
		ax.plot(self.c.t, self.tau_RB)
		ax.set_xlabel('t')
		ax.set_ylabel('tau_RB')
		ax.legend(['x','y','z'])
		
		# orientation
		N = self.c.N
		q = np.zeros((N,4))
		q_ref = np.zeros((N,4))

		print np.shape(q)

		for i in range(N):
			q[i,1:4] = self.c.q[i].v
			q[i,0] = self.c.q[i].s

			if self.q_ref[i]:
				q_ref[i,1:4] = self.q_ref[i].v
				q_ref[i,0] = self.q_ref[i].s
		
		fig = pl.figure()
		ax = fig.add_subplot(111)

		print np.shape(q[:,0])

		ax.plot(self.c.t, q[:,0],'b-')
		ax.plot(self.c.t, q[:,1],'g-')
		ax.plot(self.c.t, q[:,2],'r-')
		ax.plot(self.c.t, q[:,3],'c-')
		
		ax.plot(self.c.t, q_ref[:,0],'b--')
		ax.plot(self.c.t, q_ref[:,1],'g--')
		ax.plot(self.c.t, q_ref[:,2],'r--')
		ax.plot(self.c.t, q_ref[:,3],'c--')
		
		ax.set_xlabel('t')
		ax.set_ylabel('q')
		ax.legend(['a','b','c','d','a','b','c','d'])
	
	def plot_omega(self):
		t = self.c.t
		
		fig = pl.figure()
		ax = fig.add_subplot(111)
		
		#print np.shape(q[:,0])
		omega = self.c.omega
		q_refd = self.q_refd
		
		ax.plot(t, omega[:,0],'b-')
		ax.plot(t, omega[:,1],'g-')
		ax.plot(t, omega[:,2],'r-')
		
		ax.plot(t, q_refd[:,0],'b--')
		ax.plot(t, q_refd[:,1],'g--')
		ax.plot(t, q_refd[:,2],'r--')
		
		ax.set_xlabel('t')
		ax.set_ylabel('omega')
		
		ax.legend(['x','y','z','x_q_refd','y_q_refd','z_q_refd'])
	


