
#import time
#import numpy as np
#import itertools
#from pylab import plot, show, figure, contour
#import pylab as pl
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#from sympy import *
#import math
#import inspect

#spreader_test()

from solver import *

def grid_faces(X,Y,Z,x,y,z,nx,ny,nz):
	NX = len(X)-1
	NY = len(Y)-1

	faces = np.empty((NX,NY), dtype=object)
	print faces
	
	for i in range(NX):
		for j in range(NY):
			I = X[i]
			J = Y[j]
			M = X[i+1]
			N = Y[j+1]
			
			ll = [x[I], y[J]]
			ur = [x[M], y[N]]
			
			numx = nx[min(I,M)]
			numy = ny[min(J,N)]

			#print "I,J",I,J

			faces[i,j] = Face(1, ll, ur, z[Z], [numx, numy], [20.,20.], [20.,20.], 30.0)
	
	grid_nbrs(faces)
	
	return faces



	
	
def grid_nbrs(faces):
	nx,ny = np.shape(faces)

	for i in range(nx):
		for j in range(ny):
			if i > 0:
				faces[i,j].nbrsll[0] = faces[i-1,j]
			if i < (nx-1):
				faces[i,j].nbrsur[0] = faces[i+1,j]
			if j > 0:
				faces[i,j].nbrsll[1] = faces[i,j-1]
			if j < (ny-1):
				faces[i,j].nbrsur[1] = faces[i,j+1]


n = 10

"""
f0 = Face(1, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],10.0)
f1 = Face(2, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],20.0)
f2 = Face(3, [0.,0.],[1.,1.], 1., [n,n],[20.,20.],[20.,20.],30.0)
"""



x = [0.002,  0.008, 0.005]

y = [0.002,  0.003, 0.002, 0.02]

z = [0.010,  0.010, 0.010, 0.002, 0.01, 0.002, 0.01, 0.01, 0.01]

x = np.cumsum(np.append([0],x))
y = np.cumsum(np.append([0],y))
z = np.cumsum(np.append([0],z))

nx = [ 5,  5,  5]
ny = [ 5,  5,  5,  5]
nz = [ 5,  5,  5,  5,  5,  5,  5,  5,  5]


f_hi_xp = grid_faces([0,1,2,3], [0,1,2,3], 3, y, z, x, nx, ny, nz)

f_hi_yp = grid_faces([0,1,2,3], [1,2,3],   3, x, z, y, nx, nz, ny)



print f_hi_xp[2][0], f_hi_yp[0][1]
print f_hi_xp[2][0].nbrsur, f_hi_yp[0][1].nbrsur



f_hi_xp[2][0].nbrsur[0] = f_hi_yp[0][1]
f_hi_xp[2][1].nbrsur[0] = f_hi_yp[1][1]
f_hi_xp[2][2].nbrsur[0] = f_hi_yp[2][1]

f_hi_yp[0][1].nbrsur[1] = f_hi_xp[2][0]
f_hi_yp[1][1].nbrsur[1] = f_hi_xp[2][1]
f_hi_yp[2][1].nbrsur[1] = f_hi_xp[2][2]

print f_hi_xp[2][0], f_hi_yp[0][1]
print f_hi_xp[2][0].nbrsur, f_hi_yp[0][1].nbrsur

#print f_hi_xp
#print f_hi_yp

faces = np.concatenate((f_hi_xp.flatten(), f_hi_yp.flatten()))

#print faces


prob = Problem(faces, 'opt1')


prob.solve2(1e-2, 1e-2, True)
prob.solve2(1e-3, 1e-2, True)
prob.solve2(1e-4, 1e-2, True)

prob.plot()

#save_prob(prob, 'case_opt1')





