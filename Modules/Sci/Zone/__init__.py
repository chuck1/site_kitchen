import math
import numpy as np
import pylab as pl

import Sci.Fluids as fl

def cylinder_in_cross_flow(Re, Pr):
	#C = np.zeros(np.shape(self.Re))
	#m = np.zeros(np.shape(self.Re))
		
	#for i in range(np.size(self.Re)):
	if Re >= 40 and Re <= 4000:
		C = 0.683
		m = 0.466
	else:
		return 0 #np.zeros(np.shape(self.Re))
	
	Nu = C * Re**m * Pr**(float(1)/float(3))
	return Nu

def staggered_tube_bank(Re, Pr):
	#C = np.zeros(np.shape(self.Re))
	#m = np.zeros(np.shape(self.Re))

	#	for i in range(np.size(self.Re)):
	if Re >= 10 and Re <= 1e2:
		C = 0.9
		m = 0.4
	elif Re > 1e2 and Re <= 1e3: 
		return cylinder_in_cross_flow(Re, Pr)
	else:
		return 0

	Nu = C * Re**m * Pr**0.36
	return Nu

class RectZone:
	# fluid
	# W
	# L
	# flux
	# T_in
	# T_out

	def __init__(self):
		pass

	def copy(self, rz):
		self.W		= rz.W
		self.L		= rz.L
		self.flux	= rz.flux
		self.fluid	= rz.fluid
		self.T_in	= rz.T_in
		self.T_out	= rz.T_out
		self.fluid_operating_pressure = rz.fluid_operating_pressure

	def get_fluid_prop(self):
		TA = (self.T_in + self.T_out)*0.5
		
		self.mu = self.fluid.get('viscosity',TA)
		self.rho = self.fluid.get('density',TA)
		self.Pr = self.fluid.Pr(TA)

	def calc_mass_flow(self):
		self.dh = self.fluid.enthalpy_change(self.T_in, self.T_out)

		# global mass flow
		self.mass_flow = self.flux * self.L * self.W / self.dh

	def run(self):
		self.get_fluid_prop()
		self.calc_mass_flow()
		
		self.get_geo()
		self.get_velocity()
		self.get_Re()
		self.get_friction()
		
		self.pressure_drop()

		self.get_nusselt_number()
	
		self.stress()
	def get_Re(self):
		self.Re = self.rho * self.D_h * self.v / self.mu
		self.Re = np.array(self.Re)

	def get_velocity(self):
		# velocity through single gap or channel
		self.v = self.mass_flow / (self.rho * self.area_flow * self.NT)
	
	def disp(self):
		print "rho kg/m3       ",self.rho
		print "mu m2/s         ",self.mu
		print "mass_flow       ",self.mass_flow
		print "area_flow       ",self.area_flow
		print "v m/s           ",self.v
		print "f               ",self.f
		print "Re              ",self.Re
		print "dp bar          ",self.dp/1e5
		print "Nu              ",self.Nu
		
class Straight(RectZone):
	def __init__(self):
		pass
	def pressure_drop(self):
		self.dp = self.f * (self.L/self.D_h) * self.rho * self.v**2 / 2.0
		
class Rectangular(Straight):
	def __init__(self):
		pass

	def get_friction(self):
		self.alpha = self.H_chan / self.W_chan
		self.alpha = min(self.alpha, 1.0 / self.alpha)

		self.f = 24.0 * (1
				- 1.3553 * self.alpha
				+ 1.9467 * self.alpha**2
				- 1.7012 * self.alpha**3
				+ 0.9564 * self.alpha**4
				- 0.2537 * self.alpha**5) / self.Re
	def get_geo(self):
		self.area_flow = self.H_chan * self.W_chan

		self.NT = self.W / (self.W_chan + self.W_wall)
		
		self.perimeter_flow = 2.0 * (self.W_chan + self.H_chan)
		
		self.D_h = 4.0 * self.area_flow / self.perimeter_flow

	def get_nusselt_number(self):
		# square with uniform wall temp
		self.Nu = 2.98

	def stress(self):
		pass

	def disp(self):
		print "W_chan micron   ", self.W_chan * 1e6
		print "H_chan micron   ", self.H_chan * 1e6

		RectZone.disp(self)

class Array(RectZone):
	def __init__(self):
		pass
	def pressure_drop(self):
		self.dp = self.NL * self.f * self.rho * self.v**2 / 2.0

	def get_friction(self):
		self.f = 64.0 / self.Re

class Circular(Array):
	def __init__(self):
		pass

	def stress(self):
		self.area_planform_pin = math.pi * np.power(self.D, 2) / 4.0
		
		self.area_planform_fluid = (self.ST * self.SL) - self.area_planform_pin
		
		self.stress_pin = self.area_planform_fluid / self.area_planform_pin * self.fluid_operating_pressure
	
		self.C = 1.4

		self.stress_max = self.C * self.stress_pin

	def disp(self):
		print "stress_pin MPa  ", self.stress_pin
		print "stress_max MPa  ", self.stress_max
		
		RectZone.disp(self)

class Staggered(Circular):
	def get_geo(self):
		self.PL = self.PT * math.sqrt(3) / 2.0
		
		self.ST = self.PT * self.D
		self.SL = self.PL * self.D
		
		self.NT = self.W / self.ST
		self.NL = self.L / self.SL
		
		self.gap = self.ST - self.D

		# area of single gap
		self.area_flow = math.pi * self.gap**2 / 4.0
		
		self.D_h = self.D		

	def get_nusselt_number(self):

		fun = np.vectorize(staggered_tube_bank);

		self.Nu = fun(self.Re, self.Pr)
	
	def disp(self):
		print "D micron        ",self.D*1e6
		print "PT              ",self.PT
		print "NT              ",self.NT
		print "NL              ",self.NL

		Circular.disp(self)












