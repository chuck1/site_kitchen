#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import numpy as np
import math
import sys

#sys.path.append("/nfs/stak/students/r/rymalc/Documents/python")
sys.path.append("../")

import vector
import orbit.orbit as orbit
import orbit.system as system

#--------------
if len(sys.argv) != 2:
	print "usage: ./orbit_test.py <final_time>"
	sys.exit(0)

final_time = int(sys.argv[1])

#------------------

alt_ss   = 4.17e5
alt_moon = 3.80e8

radius_earth = 6.37100e6
radius_ss    = 1.00000e2
radius_moon  = 1.73814e3

mass_earth = 5.97219e24
mass_ss    = 4.50000e5
mass_moon  = 7.34770e22

#----------------------

earth = system.sat()
earth.init_abs( radius_earth, mass_earth, np.zeros(3) )

oc_moon = orbit.orbit_circ( earth, alt_moon )

oc_ss = orbit.orbit_circ( earth, alt_ss )
oe_ss = orbit.orbit_elip( earth, alt_moon, alt_ss )

print oe_ss.P/2.0

tweak = -0.01 * 2.0 * math.pi
theta_ss = oc_moon.theta( oe_ss.P / 2.0 ) - math.pi + tweak

print oc_ss.v
print oe_ss.vp

#-----------------------

ss = system.sat()
ss.init_rel( earth, radius_ss, oe_ss.alt_p, oe_ss.vp, 0.0 / 2.0 * math.pi, theta_ss, mass_ss )
#ss.init_rel( earth, radius_ss, oc_ss.alt, oc_ss.v, 0 * math.pi / 2, 0, mass_ss )

moon = system.sat()
moon.init_rel( earth, radius_moon, oc_moon.alt, oc_moon.v, 0.0, 0.0 / 2.0 * math.pi, mass_moon )

#-------------------

nt = 10000

ps = system.system( [earth,ss,moon] )
i = ps.run( nt, final_time )

#--------------------
# plot

fig = plt.figure()
ax = fig.gca()

#ax = Axes3D(fig)

#earth.plot_sphere( ax )
earth.plot_2dtraj( ax, i )
ss.plot_2dtraj( ax, i )
moon.plot_2dtraj( ax, i )

plt.figure()
plt.plot(ps.t[0:i],ps.c0[0:i])
plt.plot(ps.t[0:i],earth.c0[0:i])
plt.plot(ps.t[0:i],moon.c0[0:i])
plt.plot(ps.t[0:i],ss.c0[0:i])

plt.figure()
plt.plot(ps.t[0:i],moon.V[0:i])
plt.figure()
plt.plot(ps.t[0:i],moon.A[0:i])
plt.figure()
plt.plot(ps.t[0:i],ss.V[0:i])


plt.figure()
plt.plot(ps.t[0:i],ps.dt[0:i])

plt.show()






