import math
import numpy as np
import pylab as pl

#import Sci.Fluid.pressure as pres
#import Sci.Fluid.heat as heat

import Sci.Fluids as fl
import Sci.Solve.shooting as shoot

import Sci.Zone


def plot(y,y_str):
	fig = pl.figure()
	ax = fig.add_subplot(111)
	ax.plot(x,y)
	ax.set_xlabel(x_str)
	ax.set_ylabel(y_str)

def plot2(z,z_str):
	fig = pl.figure()
	ax = fig.add_subplot(111)
	con = ax.contourf(x,y,z)
	cbar = pl.colorbar(con)
	cbar.ax.set_ylabel(z_str)
	ax.set_xlabel(x_str)
	ax.set_ylabel(y_str)
	
def pressure_drop_from_diameter(D):
	ch.D = D
	ch.run()
	return ch.dp

# stress in pin

#known



fluid_pressure = 10 * 1e5

ch = Sci.Zone.Staggered()
ch.T_in = 300 + 273
ch.T_out = 600 + 273



ch.D = 5e-4
#ch.D = 4e-4 + np.arange(0.0,1.0,0.01) * 5e-4

ch.PT = 2.0
#ch.PT = np.arange(2.0, 5.0, 1.0)

# choose independent var

#ch.D, ch.PT = np.meshgrid(ch.D, ch.PT)

y = ch.PT
y_str = 'PT'

x = ch.D/1e-6
x_str = 'D micrometer'

# calc

PL = math.sqrt(3)/2.0 * ch.PT

ST = ch.PT*ch.D
SL = PL*ch.D

area_pin = math.pi * ch.D**2 / 4.0
area_fluid = ST * SL - area_pin

stress_pin = area_fluid / area_pin * fluid_pressure


# stress concentration

C = 1.4

stress_max = C * stress_pin

print stress_max

#print "stress_pin {0:f} MPa".format(stress_pin/1e6)
#print "stress_max {0:f} MPa".format(stress_max/1e6)

#print np.shape(ch.D)
#print np.shape(stress_max)



# =================
# known

fluid = fl.Fluid('ms')

# need corrent numbers

# calc

ch.W  = 1e-2
ch.L  = 1e-2
ch.flux = 4e6
ch.fluid = fl.Fluid('ms')

#ch.pressure_drop()

#plot2(stress_max/1e6, 'stress')
#plot2(ch.dp/1e5, 'dp bar')
#pl.show()


#dp = 1e5

D = shoot.shooting([2e-4, 6e-4], pressure_drop_from_diameter, 1e5 * np.ones(np.shape(ch.PT)))


ch.disp()

#Nu = heat.cross_flow_tube_bank_staggered(ch.Re, ch.Pr)

ch2 = Sci.Zone.Rectangular()
ch2.W_chan = 0.0001
ch2.H_chan = 0.0001
ch2.W_wall = 0.0001

ch2.W  = 1e-2
ch2.L  = 1e-2
ch2.flux = 4e6
ch2.fluid = fl.Fluid('ms')

ch2.run()

print "rectangular"

ch2.disp()





