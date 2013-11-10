#!/usr/bin/env python

import os
import sys

modules_dir = os.environ["HOME"] + '/Programming/Python/Modules'
sys.path.append(modules_dir)

import Sci.Fluids as Flu

# input
if len(sys.argv) < 6:
	print "usage: ./mass_flow_rate.py <temperature in> <temperature out> <length> <width> <heat flux>"
	sys.exit()

T0 = float(sys.argv[1]) #773.15
T1 = float(sys.argv[2])
l  = float(sys.argv[3])
w  = float(sys.argv[4])
q  = float(sys.argv[5])

# run



def mass_flow_rate( fluid, T0, T1, q ):
	print "hello"




#material_name = "carbon_dioxide"
#property_name = "density"
#
#material = Mod.Material()
#material.name = "carbon_dioxide"

#tree = etree.parse("material.xml")

#root = tree.getroot()
#.process_element(root)



#a = Mod.get(root,material_name,property_name)
#print "a",a

#rho = Mod.poly_eval( T1, a )
#print "rho in=%f" % rho

# polynomial coefficients for cp
#a = Mod.get(root,material_name,"cp")


#X = Mod.frange( T1, T2, 1 )
#print "X",X

#h = Mod.integ_poly(X,a)

#print "h",h

#d = 5e-4
#A = math.pi*d*d/4/2

flu = Flu.Fluid('carbon-dioxide.xml')

h = flu.enthalpy_change(T0,T1)

m = q*l*w/h

print "m %10s" % m


#v = m/rho/A
#print "v %f" % v










