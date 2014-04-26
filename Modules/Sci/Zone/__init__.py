import math
import numpy as np
import pylab as pl

import Sci.Fluids as fl

class RectZone:
	# fluid
	# W
	# L
	# flux
	# T_in
	# T_out

	def __init__(self):
		pass

	def get_fluid_prop(self):
		self.T_in = 300 + 273
		self.T_out = 600 + 273
		TA = (self.T_in + self.T_out)*0.5
		
		# self.mu = self.fluid.get('viscosity',TA) ????????
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
	def get_Re(self):
		self.Re = self.rho * self.D_h * self.v / self.mu
	def get_velocity(self):
		# velocity through single gap or channel
		self.v = self.mass_flow / (self.rho * self.area_flow * self.NT)
	
	def disp(self):
		print "v   {0:e} m/s".format(self.v)
		print "f   {0:e}".format(self.f)
		print "Re  {0:e}".format(self.Re)
		print "dp  {0:e} bar".format(self.dp/1e5)


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

		pass
	def disp(self):
		print "W_chan {0:e} m".format(self.W_chan)
		print "H_chan {0:e} m".format(self.H_chan)

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
		
		
		"""
		print "f         {0}".format(self.f)
		print "D         {0} micro".format(self.D*1e6)
		print "ST        {0} micro".format(self.ST*1e6)
		print "SL        {0} micro".format(self.SL*1e6)
		
		print "rho       {0} kg/m3".format(rho)
		print "mu        {0} m2/s".format(mu)
		print "f         {0}".format(self.f)

		print "dh        {0:e} J/kg K".format(self.dh)
		print "mass_flow {0} kg/s".format(self.mass_flow)
		print "velocity  {0} m/s".format(self.v)
		
		print "Re        {0}".format(self.Re)
		"""
		#print "pressure  {0} bar".format(self.dp/100000)
	def disp(self):
		print "D        ",self.D
		print "PT       ",self.PT
		print "NT       ",self.NT
		print "NL       ",self.NL
		print "rho      ",self.rho
		print "mu       ",self.mu
		print "mass_flow",self.mass_flow
		print "area_flow",self.area_flow
		print "v        ",self.v

		print "f        ",self.f
		print "Re       ",self.Re
		print "dp       ",self.dp












