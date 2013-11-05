#!/usr/bin/env python
import sys

# input
if len(sys.argv) < 6:
	print "usage: ./mass_flow_rate.py <temperature in> <temperature out> <length> <width> <heat flux>"
	sys.exit()

T1 = float(sys.argv[1]) #773.15
T2 = float(sys.argv[2])
l  = float(sys.argv[3])
w  = float(sys.argv[4])
q  = float(sys.argv[5])

# run
sys.path.append('/nfs/stak/students/r/rymalc/Documents/python')

import Mod
from lxml import etree
import math


def mass_flow_rate( fluid, T_in, T_out, q ):





material_name = "carbon_dioxide"
property_name = "density"

material = Mod.Material()
material.name = "carbon_dioxide"

tree = etree.parse("material.xml")

root = tree.getroot()
Mod.process_element(root)


a = Mod.get(root,material_name,property_name)
#print "a",a

rho = Mod.poly_eval( T1, a )
print "rho in=%f" % rho

# polynomial coefficients for cp
a = Mod.get(root,material_name,"cp")


X = Mod.frange( T1, T2, 1 )
#print "X",X

h = Mod.integ_poly(X,a)

#print "h",h

#d = 5e-4
#A = math.pi*d*d/4/2

m = q*l*w/h

print "m %10s" % m


#v = m/rho/A
#print "v %f" % v










