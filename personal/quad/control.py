import numpy as np

from vec import *
import quaternion as qt
import attitude
import position

class Move:
	def __init__(self, x2, thresh):
		
		self.x2 = x2
		
		self.flag_rise = False
		
		self.flag_settle = False
		self.flag_close = False
		
		self.thresh = thresh

	def start(self, c, ti):
		self.c = c
		self.ti1 = ti
		
		self.x1 = c.x[ti]
		
		self.d_mag = np.zeros(c.N)
		
		self.d_mag1 = vec.mag(self.x2 - self.x1)
		
	def step(self, ti):
		d_mag = vec.mag(self.d[ti])
		
		self.d_mag[ti] = self.x2 - self.c.x[ti]
		
		
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

	def control_law_2(self, ti, ti_0):
		# require position error
		self.ctrl_position.step(ti, ti_0)
		
		f_R = self.ctrl_position.get_force_rotor(ti, ti_0)
		
		f_R_mag = mag(f_R)
	
		q, thrust = self.process_force_reference(f_R, ti)
		
		# debug	
		#theta = np.array([math.pi/2.0, 0.0, 0.0])
		
		# set attitude reference
		self.ctrl_attitude.set_q_reference(ti, q)
		
		# get body torque
		tau_RB = self.ctrl_attitude.get_tau_RB(ti, ti_0)
		
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
		
		
		if self.ctrl_position.flag_converged or (self.ctrl_position.move is None):
			print 'new move'
			self.ctrl_position.new_move(ti)
			self.ti_0 = 0
		
		
		
		gamma = self.control_law_2(ti, self.ti_0)
		
		self.c.gamma[ti] = gamma
		
		self.ti_0 += 1
		
	def plot(self):
		#self.ctrl_x.plot()
		#self.ctrl_y.plot()
		#self.ctrl_z.plot()
		#self.ctrl_rot[0].plot()
		#self.ctrl_tilt.plot()
		pass


