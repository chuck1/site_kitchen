import numpy as np

from vec import *
import quaternion as qt
import attitude
import position

class Move:
	def __init__(self, c, ti, x1, x2):
		self.c = c
		
		self.t1 = self.c.t[ti]
		
		self.x1 = x1
		self.x2 = x2
		
		self.d1 = vec.mag(x2 - x1)
		
		self.flag_rise = False
		
		self.flag_settle = False
		self.flag_close = False
		
		self.thresh = 0.05
	def step(self, ti):
		d = self.x2 - self.c.x[ti]
		
		d_mag = vec.mag(d)
		
		if not self.flag_close:
			if d_mag < (self.d1 * self.thresh):
				self.flag_close = True
				if not self.flag_rise:
					# rise
					self.tr = self.c.t[ti] - self.t1
				else:
					# reentry
					pass
		
		
class Brain:
	def __init__(self, c):
		self.c = c

		self.ctrl_position = position.Position1(c)
		self.ctrl_attitude = attitude.Attitude3(c)
		
	def control_law_1(self, ti):
		gamma = np.zeros(4)
		
		return gamma

	def process_force_reference(self, f_R, ti):
		# input:
		# target force in inertial frame
		
		# output:
		# target quaternion orientation
		# target rotor thrust
		
		q = self.c.q[ti]
		
		# transform desired rotor force from inertial to body frame
		f_RB = q.rotate(f_R)
		
		#r = qt.Quat(v1 = qt.e2, v2 = f_RB)
		r = qt.Quat(v1 = f_RB, v2 = qt.e2)
		qn = r * q
		
		thrust = f_RB[2]
		
		if qn.isnan():
			print 'q',q.s,q.v
			print 'r',r.s,r.v
			raise ValueError('qn nan')

		return qn, thrust

	def control_law_2(self, ti):
		# require position error
		self.ctrl_position.step(ti)
		
		f_R = self.ctrl_position.get_force_rotor(ti)
		
		f_R_mag = mag(f_R)
	
		q, thrust = self.process_force_reference(f_R, ti)
		
		# debug	
		#theta = np.array([math.pi/2.0, 0.0, 0.0])
		
		# set attitude reference
		self.ctrl_attitude.set_q_reference(ti, q)
		
		# get body torque
		tau_RB = self.ctrl_attitude.get_tau_RB(ti)
		
		# calculate motor speed
		gamma = np.dot(self.c.A4inv, np.append(tau_RB, thrust))
	
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


