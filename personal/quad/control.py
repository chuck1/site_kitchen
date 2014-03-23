import numpy as np

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



class Control_Attitude:
	def __init__(self, c):
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
	
	def get_f2(self, e1, e2):
		return -np.dot(self.C2,e2) - e1
	def get_e1(self, ti):
		return np.reshape(self.e1[ti,:], (1,3))
	def get_e2(self, ti):
		return np.reshape(self.e2[ti,:], (1,3))
	def get_qref(self, ti):
		return np.reshape(self.qref[ti,:], (1,3))
	def get_qrefd(self, ti):
		return np.reshape(self.qrefd[ti,:], (1,3))
	def get_qrefdd(self, ti):
		return np.reshape(self.qrefdd[ti,:], (1,3))
	def step(self, ti):
		# refernce values must be set before stpping
		
		dt = self.t[ti] - self.t[ti]

		self.qrefp[ti] = (self.get_qref(ti) - self.get_qref(ti-1)) / dt
		
		if ti > 1:
			self.qrefpp[ti] = (self.get_qrefp(ti) - self.get_qrefp(ti-1)) / dt
		
		self.chi1[ti] = self.chi1[ti-1] + self.e1[ti] * dt

	def get_tau_rotor_body(self, ti):
		
		e1 = self.get_e1(ti)
		e2 = self.get_e2(ti)
		
		f2 = self.get_f2(e1,e2)
		
		chi1 = self.get_chi1(ti)
		
		C1 = self.C1
		L1 = self.L1
		qrefdd = self.get_qrefdd(self, ti)
			
		A3 = self.c.get_A3(ti)
		A3d = self.c.get_A3d(ti)
		A3inv = self.c.get_A3inv(ti)
		
		temp = -f2 + np.dot(np.dot(C1, A3), e2 - np.dot(C1,e1) - np.dot(L1,chi1)) + qrefdd + np.dot(L1,e1) - np.dot(A3d,omega)
		
		tau_RB = np.dot(np.dot(I, A3inv), temp) + np.cross(omega, np.dot(I, omega))
	
		return tau_RB

class Control_Position:
	def __init__(self, c):
		C5_11 = 2.0
		C5_22 = 2.0
		C5_33 = 3.5
		C6_11 = 0.5
		C6_22 = 0.5
		C6_33 = 1.5
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
		
		
	def get_f6(self, e5, e6):
		return -np.dot(self.C6,e6) - e5
	def step(self, ti):
		self.e5[ti] = self.xref[ti] - self.c.x[ti]
		self.e6[ti] = self.vref[ti] - self.c.v[ti]
		self.chi5[ti] = self.chi5[ti-1] + self.e5[ti] * dt 
	def get_force_rotor(self, ti):
		e5 = self.get_e5(ti)
		e6 = self.get_e6(ti)

		f6 = self.get_f6(e5,e6)

		C5 = self.C5
		L5 = self.L5

		f_R = c.m * (-f6 + np.dot(C5, e6 - np.dot(C5, e5) - np.dot(L5, chi5)) + xrefdd + np.dot(L5, e5) - c.g - FD / m)
		return f_R

		
		
		
		
class Brain:
	def __init__(self, c):
		self.c = c

		self.ctrl_position = Control_Position(c)
		self.ctrl_attitude = Control_Attitude(c)
		
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

	def get_force_rotor_body(self, f_R):
		
		# transform desired rotor force from inertial to body frame
		f_RB = self.c.q.rotate(f_R)
		
		fz_RB = f_RB[2]
		
		return fz_RB
	def control_law_1(self, ti):
		gamma = np.zeros(4)
		
		return gamma
	def control_law_2(self, ti):
		# require position error
		self.ctrl_position.step(ti)
		
		f_R = self.ctrl_position.get_force_rotor(ti)
		
		q = Quat()
		q.set_from_unit_vectors(np.array([0,0,1]), normalize(f_R))
		
		# set attitude reference for previous step
		self.ctrl_attitude.qref[ti] = q
		
		# require attitude error
		self.ctrl_attitude.step(ti)
		
		tau_RB = self.ctrl_attitude.get_tau_rotor_body(ti)
		
		fz_RB = self.get_force_rotor_body(f_R)
		
		gamma = np.dot(self.A4inv, np.append(tau_RB, fz_RB))
		
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


