import time
import numpy as np
import itertools
from pylab import plot, show, figure, contour
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import math
import inspect
import pickle
import signal
import sys

from unit_vec import *
from Face import *

alpha = 1.2
alpha_src = 1.4

it_max_1 = 1000
it_max_2 = 1000

class NoIntersectError(Exception):
	pass

class EdgeError(Exception):
	def __init__(self, rev):
		self.rev = rev

def align(ind1, ind2):
	ver = False
	#ver = True

	s = max(min(ind1), min(ind2))
	e = min(max(ind1), max(ind2))
	
	if ver:
		print "ind1", ind1
		print "ind2", ind2
		print "s", s, "e", e
	
	try:
		s1 = ind1.index(s)
		e1 = ind1.index(e)
		s2 = ind2.index(s)
		e2 = ind2.index(e)
	except ValueError:
		raise NoIntersectError
	
	if ver:
		print "s1", s1, "e1", e1
		print "s2", s2, "e2", e2

	if s == e:
		raise EdgeError(False if s1 > s2 else True)
	
	d1 = sign(e1-s1)
	d2 = sign(e2-s2)
	
	if ver:
		print ind1
		print ind2

		print "min",min(ind1), min(ind2), "s", s
		print "max",max(ind1), max(ind2), "e", e
	
		print s1, e1, d1
		print s2, e2, d2
	
	i1 = lambda i: s1 + (i - (d1-1)/2) * d1
	i2 = lambda i: s2 + (i - (d2-1)/2) * d2
	
	r1 = []
	r2 = []
	
	for i in range(abs(e1-s1)):
		if ver:
			print "1:", i1(i), "'", ind1[i1(i)], ind1[i1(i)+1], "'" #, ind1[i+s1]
			print "2:", i2(i), "'", ind2[i2(i)], ind2[i2(i)+1], "'" #, ind2[i+s2]
		
		r1.append(i1(i))
		r2.append(i2(i))

	return r1,r2
	
	
	
def nice_axes(a, b):
	p = math.floor(math.log10(b - a))
	a = nice_lower(a, p)
	b = nice_upper(b, p)
	return a, b

def nice_upper(a, p):
	a = a / 10**p
	a = math.ceil(a)
	a = a * 10**p
	return a
	
def nice_lower(a, p):
	a = a / 10**p
	a = math.floor(a)
	a = a * 10**p
	return a
	
def load_prob(filename):
	f = open(filename, 'r')
	o = pickle.load(f)
	return o





def spreader_test():
	x = np.linspace(-1.,1.)
	y = np.linspace(-1.,1.)
	X,Y = np.meshgrid(x,y)
	
	Z = source_spreader(X,Y,1,1,2,2)

	con = pl.contourf(X,Y,Z)
	pl.colorbar(con)
	
	pl.show()
	

class Problem:
	def __init__(self, name, k):
		self.name = name
		self.k = k
		self.faces = []
		signal.signal(signal.SIGINT, self)
	def createPatch(self, normal, indices, x, nx):
		p = Patch(normal, indices, x, nx, self.k)
		self.faces += list(p.faces.flatten())
		return p
	def __call__(self, signal, frame):
		print "saving"
		self.save()
		sys.exit(0)
		
	def temp_max(self):
		T = float("-inf")
		for f in self.faces:
			T = max(f.temp_max(), T)
		
		return T
	def temp_min(self):
		T = float("inf")
		for f in self.faces:
			T = min(f.temp_min(), T)
		
		return T
	def grad_max(self):
		T = float("-inf")
		for f in self.faces:
			T = max(f.grad_max(), T)
		
		return T
	def grad_min(self):
		T = float("inf")
		for f in self.faces:
			T = min(f.grad_min(), T)
		
		return T

	def plot(self):
		a, b = nice_axes(self.temp_min(), self.temp_max())
		V = np.linspace(a, b, 21)
		
		a, b = nice_axes(self.grad_min(), self.grad_max())
		Vg = np.linspace(a, b, 21)
		
		
		for f in self.faces:
			f.plot(V)
			#f.plot_grad(Vg)
		
		pl.show()

	def plot3(self):
		T_max = self.temp_max()
		
		fig = figure()
		ax = Axes3D(fig)
		
		for f in self.faces:
			f.plot3(ax, T_max)
		
		
	def solve(self, cond, ver=True, R_outer=0.0):
		
		#fig = pl.figure()
		#ax = fig.add_subplot(111)
		#hl, = ax.plot([],[])
		#pl.ion()
		#pl.show()
		
		R = np.array([])
	
		for it in range(it_max_1):
			R = np.append(R, 0.0)
			
			for face in self.faces:
				R[-1] = max(face.step(), R[-1])
			
			if ver:
				print "{0:3d} {1:8e} {2:8e}".format(it, R_outer, R[-1])
			
			#hl.set_xdata(np.append(hl.get_xdata(), it))
			#hl.set_ydata(np.append(hl.get_ydata(), R))
			#pl.draw()
			
			if math.isnan(R[-1]):
				raise ValueError('nan')
			
			if R[-1] < cond:
				break
		
		return it
		
		#if ver:
			#pl.semilogy(R)
			#pl.show()
		
	
	def solve3(self, cond1_final, cond2_final, ver = False):
		cond1 = 1
		cond2 = 1e-4
		
		it_2 = self.solve2(cond1_final, cond2, ver)

	def solve2(self, cond1_final, cond2, ver = False):
		cond1 = 1
		
		it_cond = 2
		
		R = 1.0
		for it_2 in range(it_max_2):
			
			cond1 = R / 10.0 # target residual for inner loop is proportional to current residual for outer loop
			
			it_1 = self.solve(cond1, ver, R)
			
			#if it_1 < it_cond and cond1 > cond1_final:
			#cond1 /= 10**0.2
			
			
			
			R = 0.0
			
			for f in self.faces:
				f.reset_s()
				R = max(math.fabs(f.mean() - f.mean_target) / f.mean_target, R)
			
			print "{0:3d} {1:8e}".format(it_2,R)
			
			if math.isnan(R):
				raise ValueError('nan')
			
			if R < cond2:
				break
		
		return it_2

	def save(self):
		f = open('case_' + self.name, 'w')
		pickle.dump(self, f)

class Patch(LocalCoor):
	def __init__(self, normal, indices, x, nx, k):
		LocalCoor.__init__(self, normal)
		
		self.k = k
		
		self.indices = indices
		
		NX = len(indices[self.x])-1
		NY = len(indices[self.y])-1
		
		faces = np.empty((NX,NY), dtype=object)
		
		for i in range(NX):
			for j in range(NY):
				I = indices[self.x][i]
				J = indices[self.y][j]
				M = indices[self.x][i+1]
				N = indices[self.y][j+1]
				
				Is = min(I,M)
				Js = min(J,N)
				Ms = max(I,M)
				Ns = max(J,N)
				
				ext = [[x[self.x][Is], x[self.x][Ms]], [x[self.y][Js], x[self.y][Ns]]]
				
				numx = nx[self.x][min(I,M)]
				numy = nx[self.y][min(J,N)]
				
				#print "I,J",I,J
				
				faces[i,j] = Face(1, ext, x[self.z][indices[self.z]], [numx, numy], [[20.,20.], [20.,20.]], 30.0, self.k)
		
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
	ver = False
	#ver = True

	if ver:
		print "stitch"	
		print "patch1.Z", patch1.Z
		print "patch2.Z", patch2.Z
	
	if patch1.Z == patch2.Z:
		stitch_ortho(patch1, patch2)
		return

	# global direction parallel to common edge
	P = cross(patch1.Z, patch2.Z)

	pg,_ = v2is(P)

	PL1 = patch1.glo_to_loc(P)
	PL2 = patch2.glo_to_loc(P)

	og1 = patch2.z
	og2 = patch1.z
	
	ol1,_ = v2is(patch1.glo_to_loc(patch2.Z))
	ol2,_ = v2is(patch2.glo_to_loc(patch1.Z))
	
	if ver: print "ol1", ol1, "ol2", ol2

	if patch1.indices[og1].index(patch2.indices[patch2.z]) == 0:
		sol1 = -1
	else:
		sol1 = 1
	
	if patch2.indices[og2].index(patch1.indices[patch1.z]) == 0:
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
	
	r1, r2 = align(patch1.indices[pg], patch2.indices[pg])
	
	for i1, i2 in zip(r1, r2):
		
		ind1[pl1] = i1
		ind2[pl2] = i2

		patch1.faces[ind1[0],ind1[1]].nbrs[ol1,(sol1+1)/2] = patch2.faces[ind2[0],ind2[1]]
		
		patch2.faces[ind2[0],ind2[1]].nbrs[ol2,(sol2+1)/2] = patch1.faces[ind1[0],ind1[1]]

def stitch_ortho(patch1, patch2):
	ver = False
	#ver = True

	if ver: print "stitch_ortho"

	ind1 = [0,0]
	ind2 = [0,0]
	
	try:
		r01,r02 = align(patch1.indices[patch1.x], patch2.indices[patch2.x])
	except EdgeError as e:
		o = 0
		p = 1
		rev = e.rev
	except:
		raise
	else:		
		r1, r2 = r01, r02
	
	try:
		r11,r12 = align(patch1.indices[patch1.y], patch2.indices[patch2.y])
	except EdgeError as e:
		o = 1
		p = 0
		rev = e.rev
	except:
		raise
	else:
		r1, r2 = r11, r12
	
	
	if rev:
		ind1[o] = 0
		ind2[o] = patch2.npatch[o] - 1

		sol1 = -1
		sol2 = 1
	else:
		ind1[o] = patch1.npatch[o] - 1
		ind2[o] = 0
		
		sol1 = 1
		sol2 = -1

	if ver:
		print "o   ",o
		print "sol1",sol1
		print "sol2",sol2
	
	for i1, i2 in zip(r1, r2):
		ind1[p] = i1
		ind2[p] = i2
		
		f1 = patch1.faces[ind1[0],ind1[1]]
		f2 = patch2.faces[ind2[0],ind2[1]]
		
		if not f1.nbrs[o,(sol1+1)/2] is None:
			print "face1", ind1
			print "face2", ind2
			raise ValueError('nbr not none')
		if not f2.nbrs[o,(sol2+1)/2] is None:
			
			raise ValueError('nbr not none')

		
		f1.nbrs[o,(sol1+1)/2] = f2
		f2.nbrs[o,(sol2+1)/2] = f1
		
def test_localcoor(z):
	lc = LocalCoor(z)

	print "g   l"
	print "1   ",lc.glo_to_loc(1)
	print "2   ",lc.glo_to_loc(2)
	print "3   ",lc.glo_to_loc(3)
	
	print "l   g"
	print "1   ",lc.loc_to_glo(1)
	print "2   ",lc.loc_to_glo(2)
	print "3   ",lc.loc_to_glo(3)


if __name__ == '__main__':
	test_localcoor(2)
	

