
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

class Patch(LocalCoor):
	def __init__(self, normal, indices, Zind, x, y, z, nx, ny, nz):
		LocalCoor.__init__(self, normal)
		
		self.indices = indices
		self.Zind = Zind

		NX = len(indices[0])-1
		NY = len(indices[1])-1
		
		faces = np.empty((NX,NY), dtype=object)
		
		for i in range(NX):
			for j in range(NY):
				I = indices[0][i]
				J = indices[1][j]
				M = indices[0][i+1]
				N = indices[1][j+1]
				
				Is = min(I,M)
				Js = min(J,N)
				Ms = max(I,M)
				Ns = max(J,N)
				
				ext = [[x[Is], x[Ms]], [y[Js], y[Ns]]]
				
				numx = nx[min(I,M)]
				numy = ny[min(J,N)]
				
				#print "I,J",I,J
				
				faces[i,j] = Face(1, ext, z[Zind], [numx, numy], [[20.,20.], [20.,20.]], 30.0)
				
		
		self.npatch = np.array([NX,NY])

		self.faces = faces;

		self.grid_nbrs()
	
		
	def grid_nbrs(self):
		nx,ny = np.shape(self.faces)
	
		for i in range(nx):
			for j in range(ny):
				if i > 0:
					self.faces[i,j].nbrs[0,0] = self.faces[i-1,j]
				if i < (nx-1):
					self.faces[i,j].nbrs[0,1] = self.faces[i+1,j]
				if j > 0:
					self.faces[i,j].nbrs[1,0] = self.faces[i,j-1]
				if j < (ny-1):
					self.faces[i,j].nbrs[1,1] = self.faces[i,j+1]
	


def stitch(patch1, patch2):
	print "stitch"	
	print "patch1.Z", patch1.Z
	print "patch2.Z", patch2.Z
	
	if patch1.Z == patch2.Z:
		stitch_ortho(patch1, patch2)
		return

	# global direction parallel to common edge
	P = cross(patch1.Z, patch2.Z)
	
	PL1 = patch1.glo_to_loc(P)
	PL2 = patch2.glo_to_loc(P)

	ol1,_ = v2is(patch1.glo_to_loc(patch2.Z))
	ol2,_ = v2is(patch2.glo_to_loc(patch1.Z))
	
	print "ol1", ol1, "ol2", ol2

	if patch1.indices[ol1].index(patch2.Zind) == 0:
		sol1 = -1
	else:
		sol1 = 1
	
	if patch2.indices[ol2].index(patch1.Zind) == 0:
		sol2 = -1
	else:
		sol2 = 1
	
	pl1,spl1 = v2is(PL1)
	pl2,spl2 = v2is(PL2)

	n1 = patch1.npatch[pl1]
	n2 = patch2.npatch[pl2]
	
	ind1 = [0,0]
	ind2 = [0,0]
	
	ind1[ol1] = 0 if sol1 < 0 else (patch1.npatch[ol1] - 1)
	ind2[ol2] = 0 if sol2 < 0 else (patch2.npatch[ol2] - 1)
	
	r1, r2 = align(patch1.indices[pl1], patch2.indices[pl2])
	
	for i1, i2 in zip(r1, r2):
		
		ind1[pl1] = i1
		ind2[pl2] = i2

		patch1.faces[ind1[0],ind1[1]].nbrs[ol1,(sol1+1)/2] = patch2.faces[ind2[0],ind2[1]]
		
		patch2.faces[ind2[0],ind2[1]].nbrs[ol2,(sol2+1)/2] = patch1.faces[ind1[0],ind1[1]]

def stitch_ortho(patch1, patch2):
	print "stitch_ortho"

	ind1 = [0,0]
	ind2 = [0,0]

	try:
		r01,r02 = align(patch1.indices[0], patch2.indices[0])
	except EdgeError as e:
		o = 0
		p = 1
	
		rev = e.rev

		if e.rev:
			ind1[o] = 0
			ind2[o] = patch2.npatch[o] - 1
		else:
			ind1[o] = patch1.npatch[o] - 1
			ind2[o] = 0

	else:		
		r1, r2 = r01, r02
	
	try:
		r11,r12 = align(patch1.indices[1], patch2.indices[1])
	except EdgeError as e:
		o = 1
		p = 0

		rev = e.rev

		if e.rev:
			ind1[o] = 0
			ind2[o] = patch2.npatch[o] - 1
		else:
			ind1[o] = patch1.npatch[o] - 1
			ind2[o] = 0
	else:		
		r1, r2 = r11, r12
	
	if rev:
		sol1 = -1
		sol2 = 1
	else:
		sol1 = 1
		sol2 = -1

	

	for i1, i2 in zip(r1, r2):
		ind1[p] = i1
		ind2[p] = i2
		
		patch1.faces[ind1[0],ind1[1]].nbrs[o,(sol1+1)/2] = patch2.faces[ind2[0],ind2[1]]
		
		patch2.faces[ind2[0],ind2[1]].nbrs[o,(sol2+1)/2] = patch1.faces[ind1[0],ind1[1]]
		
		
	
	


x = [0.002,  0.008, 0.005]

y = [0.002,  0.003, 0.002, 0.02]

z = [0.010,  0.010, 0.010, 0.002, 0.01, 0.002, 0.01, 0.01, 0.01]

x = np.cumsum(np.append([0],x))
y = np.cumsum(np.append([0],y))
z = np.cumsum(np.append([0],z))

nx = [ 5,  5,  5]
ny = [ 5,  5,  5,  5]
nz = [ 5,  5,  5,  5,  5,  5,  5,  5,  5]

# zi z inner
# zo z outer

# inlet
f_hi_xp   = Patch( 1, [[0,1,2,3], [0,1,2,3]], 3, y, z, x, ny, nz, nx)

f_hi_yp_1 = Patch( 2, [[0,1,2,3], [1,2,3]],   3, z, x, y, nz, nx, ny)
f_hi_yp_2 = Patch( 2, [[0,1],     [0,1]],     3, z, x, y, nz, nx, ny)
f_hi_yp_3 = Patch( 2, [[2,3],     [0,1]],     3, z, x, y, nz, nx, ny)

f_hi_ym   = Patch(-2, [[3,2,1,0], [3,2,1,0]], 0, x, z, y, nx, nz, ny)

f_hi_zo   = Patch(-3, [[3,2,1,0], [3,2,1,0]], 0, y, x, z, ny, nx, nz)

f_hi_zi_1 = Patch( 3, [[2,3],     [0,1,2,3]], 3, x, y, z, nx, ny, nz)
f_hi_zi_2 = Patch( 3, [[0,1,2],   [0,1]],     3, x, y, z, nx, ny, nz)
f_hi_zi_3 = Patch( 3, [[0,1,2],   [2,3]],     3, x, y, z, nx, ny, nz)

stitch(f_hi_xp,   f_hi_yp_1)
stitch(f_hi_xp,   f_hi_ym)
stitch(f_hi_xp,   f_hi_zo)
stitch(f_hi_xp,   f_hi_zi_1)

stitch(f_hi_yp_1, f_hi_yp_2)
stitch(f_hi_yp_1, f_hi_yp_3)
stitch(f_hi_yp_1, f_hi_zo)
stitch(f_hi_yp_1, f_hi_zi_1)
stitch(f_hi_yp_1, f_hi_zi_3)

stitch(f_hi_yp_2, f_hi_zo)

stitch(f_hi_ym,   f_hi_zo)

stitch(f_hi_zi_1, f_hi_zi_2)
stitch(f_hi_zi_1, f_hi_zi_3)

#outlet
f_ho_xp   = Patch( 1, [[0,1,2,3], [6,7,8,9]], 3, y, z, x, ny, nz, nx)

f_ho_yp_1 = Patch( 2, [[6,7,8,9], [1,2,3]],   3, z, x, y, nz, nx, ny)
f_ho_yp_2 = Patch( 2, [[6,7],     [0,1]],     3, z, x, y, nz, nx, ny)
f_ho_yp_3 = Patch( 2, [[8,9],     [0,1]],     3, z, x, y, nz, nx, ny)

f_ho_ym   = Patch(-2, [[3,2,1,0], [9,8,7,6]], 0, x, z, y, nx, nz, ny)

f_ho_zo   = Patch(-3, [[3,2,1,0], [3,2,1,0]], 9, y, x, z, ny, nx, nz)

f_ho_zi_1 = Patch( 3, [[2,3],     [0,1,2,3]], 6, x, y, z, nx, ny, nz)
f_ho_zi_2 = Patch( 3, [[0,1,2],   [0,1]],     6, x, y, z, nx, ny, nz)
f_ho_zi_3 = Patch( 3, [[0,1,2],   [2,3]],     6, x, y, z, nx, ny, nz)

stitch(f_ho_xp,   f_ho_yp_1)
stitch(f_ho_xp,   f_ho_ym)
stitch(f_ho_xp,   f_ho_zo)
stitch(f_ho_xp,   f_ho_zi_1)

stitch(f_ho_yp_1, f_ho_yp_2)
stitch(f_ho_yp_1, f_ho_yp_3)
stitch(f_ho_yp_1, f_ho_zo)
stitch(f_ho_yp_1, f_ho_zi_1)
stitch(f_ho_yp_1, f_ho_zi_3)

stitch(f_ho_yp_2, f_ho_zo)

stitch(f_ho_ym,   f_ho_zo)

stitch(f_ho_zi_1, f_ho_zi_2)
stitch(f_ho_zi_1, f_ho_zi_3)






#print f_hi_xp
#print f_hi_yp

faces = np.concatenate((
	f_hi_xp.faces.flatten(),
	f_hi_yp.faces.flatten(),
	f_hi_ym.faces.flatten()
	))

#print faces


prob = Problem(faces, 'opt1')

prob.solve2(1e-4, 1e-2, True)

prob.plot()

#save_prob(prob, 'case_opt1')





