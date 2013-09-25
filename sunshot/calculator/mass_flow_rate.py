import sys

sys.path.append('/nfs/stak/students/r/rymalc/Documents/python')

print sys.path


import Mod
from lxml import etree
import math

material_name = "carbon_dioxide"
property_name = "density"

material = Mod.Material()
material.name = "carbon_dioxide"

tree = etree.parse("material.xml")

root = tree.getroot()
Mod.process_element(root)


a = Mod.get(root,material_name,property_name)
print "a",a

T = 773.15


rho = Mod.poly_eval(T,a)
print "rho",rho

a = Mod.get(root,material_name,"cp")
print "a",a

X = Mod.frange(T,T+150,1)
print "X",X

h = Mod.integ_poly(X,a)

print "h",h






q = 1e6
l = 1e-2
w = 5e-4
d = 5e-4

A = math.pi*d*d/4/2

m = q*l*w/h
print "m %f" % m

v = m/rho/A
print "v %f" % v

