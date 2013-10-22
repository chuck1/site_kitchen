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


#--------------
if len(sys.argv) != 3:
	print "usage: ./orbit_test.py <final_time> <time_step>"
	sys.exit(0)

final_time = int(sys.argv[1])
time_step = int(sys.argv[2])

#------------------

alt_ss = 4.17e5
alt_moon = 3.8e8

radius_earth = 6.371e6
radius_ss = 100
radius_moon = 1.73814e3

mass_earth = 5.97219e24
mass_ss = 4.5e5
mass_moon = 7.3477e22

#----------------------

earth = orbit.sat()
earth.init_abs( radius_earth, mass_earth, np.zeros(3) )

oc_moon = orbit.orbit_circ( earth, alt_moon )

oc_ss = orbit.orbit_circ( earth, alt_ss )
oe_ss = orbit.orbit_elip( earth, alt_moon, alt_ss )

print oc_ss.v
print oe_ss.vp

ss = orbit.sat()
ss.init_rel( earth, radius_ss, oe_ss.alt_p, oe_ss.vp, 0 * math.pi / 2, 0, mass_ss )
#ss.init_rel( earth, radius_ss, oc_ss.alt, oc_ss.v, 0 * math.pi / 2, 0, mass_ss )

moon = orbit.sat()
moon.init_rel( earth, radius_moon, oc_moon.alt, oc_moon.v, 0, 0.0 / 2.0 * math.pi, mass_moon )

#-------------------

nt = final_time / time_step

ps = orbit.system( [earth,ss,moon] )
ps.run( nt, time_step )

#--------------------
# plot

fig = plt.figure()
ax = fig.gca()

#ax = Axes3D(fig)

#earth.plot_sphere( ax )
earth.plot_2dtraj( ax )
ss.plot_2dtraj( ax )
moon.plot_2dtraj( ax )

#plt.figure()
#plt.plot(t,d)

plt.show()






