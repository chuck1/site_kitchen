import math
import numpy as np

import Sci.Fluids as fl

def pressure_drop(PT,D):

	PL = PT * math.sqrt(3) / 2.0
	
	ST = PT * D
	SL = PL * D
	
	NT = W / ST
	NL = L / SL
	
	gap = ST - D
	
	area_flow = math.pi * gap**2
	
	mass_flow = flux * L * W / dh
	
	v = mass_flow / rho / area_flow
	
	Re = rho * area_flow * v / mu
	
	f = 64.0 / Re
	
	dp = NL * f * rho * v**2 / 2.0
	
	print "f         {0}".format(f)
	print "D         {0} micro".format(D*1e6)
	print "ST        {0} micro".format(ST*1e6)
	print "SL        {0} micro".format(SL*1e6)
	
	print "dh        {0:e} J/kg K".format(dh)
	print "mass_flow {0} kg/s".format(mass_flow)
	print "velocity  {0} m/s".format(v)
	print "pressure  {0} bar".format(dp/100000)
	print "Re        {0}".format(Re)
	


# known

fluid = fl.Fluid('ms')

# need corrent numbers
rho = 1000
dh = fluid.enthalpy_change(300, 600)
mu = 1e-5

# have corrent numbers
flux = 4e6
L = 1e-2
W = 1e-2


# independent variables

PT = 1.9
D  = 3e-4

# calc

pressure_drop(PT,D)



