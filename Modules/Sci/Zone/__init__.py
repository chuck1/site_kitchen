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

	def calc_mass_flow(self):
		self.dh = self.fluid.enthalpy_change(self.T_in, self.T_out)
		self.mass_flow = self.flux * self.L * self.W / self.dh

class Array(RectZone):
	def __init__(self):
		pass

class Circular(Array):
	def __init__(self):
		pass

class Staggered(Circular):
	def pressure_drop(self):
		
		self.calc_mass_flow()

		self.PL = self.PT * math.sqrt(3) / 2.0
		
		self.ST = self.PT * self.D
		self.SL = self.PL * self.D
		
		self.NT = self.W / self.ST
		self.NL = self.L / self.SL
		
		self.gap = self.ST - self.D
		
		self.area_flow = math.pi * self.gap**2

		T0 = 300 + 273
		T1 = 600 + 273
		TA = (T0+T1)*0.5
	
		self.Pr = self.fluid.Pr(TA)
		
		
		self.mu = self.fluid.get('viscosity',TA)
		self.rho = self.fluid.get('density',TA)
		
		self.v = self.mass_flow / self.rho / self.area_flow
		
		self.Re = self.rho * self.area_flow * self.v / self.mu
		
		self.f = 64.0 / self.Re
		
		self.dp = self.NL * self.f * self.rho * self.v**2 / 2.0
		
		
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
		print "D ",self.D
		print "PT",self.PT
		
		print "rho      ",self.rho
		print "mu       ",self.mu
		print "area_flow",self.area_flow
		print "v        ",self.v

		print "f ",self.f
		print "Re",self.Re
		print "dp",self.dp












