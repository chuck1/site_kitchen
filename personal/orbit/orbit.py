#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import itertools
import numpy as np
import math
import sys

#sys.path.append("/nfs/stak/students/r/rymalc/Documents/python")
sys.path.append("../../")

import vector
import orbit_mod as om

earth = om.sat()
earth.init_abs( 6.371e6, 5.97219e24, np.zeros(3) )

o = om.orbit_elip( earth, 3.8e8, 4.17e5 )

ss = om.sat()
#ss.init_rel( earth, 100, 417000, 7660, 0 * math.pi / 2, 0, 450000 )
ss.init_rel( earth, 100, 417000, o.vp, 0 * math.pi / 2, 0, 450000 )

moon = om.sat()
moon.init_rel( earth, 1.73814e3, 3.8e8, 1.022e3, 0, 0.0 / 2.0 * math.pi, 7.3477e22 )

ps = om.system( [earth,ss,moon] )
ps.run( 9000, 100 )

# plot

#fig = plt.figure()
#ax = fig.gca()

#ax = Axes3D(fig)

#earth.plot_sphere( ax )
#earth.plot_2dtraj( ax )
#ss.plot_2dtraj( ax )
#moon.plot_2dtraj( ax )

#plt.figure()
#plt.plot(t,d)

#plt.show()

#-------------------------------------

fig = plt.figure()
ax = fig.gca()

def init():
	return ss.init_anim(ax)

def animate(i):
	return ss.animate(i)
	

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)

filename = 'orbit.mp4'

#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
anim.save( filename, fps=30 )

plt.show()






