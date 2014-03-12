from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits

from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib

import pylab

import numpy as np
import inspect



fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(-5, 5, .5)
Y = np.arange(-5, 5, .5)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
Gx, Gy = np.gradient(Z) # gradients with respect to x and y
G = (Gx**2+Gy**2)**.5  # gradient magnitude
N = G/G.max()  # normalize 0..1



if 1:
	FC = cm.jet(N.flatten())
	print FC[0]
	print np.shape(FC)

if 0:
	FC = cm.jet(N)
	print FC[0]
	print np.shape(FC)


#print np.shape(FC)


#FC.fill(clr.ColorConverter().to_rgb('0.5'))

if 0:
	FC = np.empty(np.prod(np.shape(N)), dtype=object)
	FC.fill((1.,0.,0.))

	print FC[0]
	print np.shape(FC)

if 0:
	FC = np.empty(np.shape(N), dtype=object)
	FC.fill((1.,0.,0.))
	FC.fill("1.,0.,0.")

	print FC[0,0]
	print np.shape(FC)


#print inspect.getargspec(Axes3D.plot_surface)
print "matplotlib version ",matplotlib.__version__

#FC = np.zeros(np.shape(N))
#FC.fill((1.,0.,0.))

surf = ax.plot_surface(	X, Y, Z, rstride=1, cstride=1, facecolors=FC, antialiased=False, shade=False)
plt.show()

