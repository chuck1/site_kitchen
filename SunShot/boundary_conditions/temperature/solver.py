import time
import numpy as np
import itertools
from pylab import plot, show, figure, contour
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#from sympy import *
import math
import inspect
import pickle
import signal
import sys

k = 10

alpha = 1.2
alpha_src = 1.2

it_max_1 = 1000
it_max_2 = 1000

class NoIntersectError:
	a = 0
class EdgeError:
	rev = 0

def sign(x):
	return -1 if x < 0 else 1

def align(ind1, ind2):
	#ver = False
	ver = True

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
		err = EdgeError
		err.rev = True if s1 > s2 else False
		raise err
	
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
	
class LocalCoor:
	# store as [[-1, 1],[-2, 2]]
	
	# xyz
	
	def __init__(self, Z):
		self.Z = Z
		self.X = nxt(self.Z)
		self.Y = nxt(self.X)
		
	def glo_to_loc(self, G):
		sg = sign(G)
		sz = sign(self.Z)
		
		d = nxt_dist(abs(self.Z), abs(G))
		
		L = sg * nxt(3 * sz, d)
		
		return L
		
	def loc_to_glo(self, L):
		G = sign(L) * nxt(self.Z, abs(L) % 3)
		return G
	
	
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

def source_spreader(x,y,a,b,m,n):
	
	u = (1 - (x / a)**m) * (1 - (y / b)**n) * (m + 1) / m * (n + 1) / n
	
	return u

def is2v(i,s):
	return (i + 1) * s
def v2is(v):
	return abs(v) - 1, sign(v)
	
def fwd(A, n):
	a,s = v2is(A)

	b = (a + n) % 3
	
	B = is2v(b,s)
	return B

def fwd_dist(A, B):
	a,sa = v2is(A)
	b,sb = v2is(B)
	
	d = b - a
	d = d if d > 0 else d + 3
	return d

def bwd(A, n):
	B = fwd(A, 2 * n)
	return B

def bwd_dist(A, B):
	d = fwd_dist(B, A)

def nxt(A, n = 1):
	if A > 0:
		return fwd(A, n)
	else:
		return bwd(A, n)

def nxt_dist(A, B):
	if A > 0:
		return fwd_dist(A, B)
	else:
		return bwd_dist(A, B)


	
def cross(A,B):
	#print A,B
	
	a,sa = v2is(A)
	b,sb = v2is(B)
	
	if b == (a+1) % 3:
		c = ((a+2) % 3) + 1
	else:
		c = ((a+1) % 3) + 1
		c = -c
	
	c *= sa * sb
	
	#print a, b, c

	return c

class Face(LocalCoor):
	def __init__(self, normal, ext, z, n, T_bou, mean_target):
		
		#self.ll = np.array(ll)
		#self.ur = np.array(ur)
		
		self.ext = np.array(ext)
		
		self.z = z
		
		self.n = np.array(n)
		self.d = (self.ext[:,1] - self.ext[:,0]) / np.float32(self.n)
		self.T = np.ones(n) * mean_target
		
		if any(self.d < 0):
			print self.ll
			print self.ur
			print self.d
			raise ValueError('bad')
		
		self.T_bou = np.array(T_bou)

		self.nbrs = np.empty((2,2), dtype=object)
		
		
		self.S = 0
		self.s = np.zeros(n)
		
		
		self.mean_target = mean_target
		
		# source
		self.l = np.array([
			(self.ext[0,1] - self.ext[0,0]) / 2.0,
			(self.ext[1,1] - self.ext[1,0]) / 2.0])
		
		
		a = self.l[0] / 2.
		b = self.l[1] / 2.
		
		x = np.linspace(self.d[0] / 2. - a, a - self.d[0] / 2., self.n[0])
		y = np.linspace(self.d[1] / 2. - b, b - self.d[1] / 2., self.n[1])
		X,Y = np.meshgrid(x,y)
		
		self.s = source_spreader(X,Y,a,b,2,2)

		self.Src = 0

		# coordinates
		LocalCoor.__init__(self, normal)

	def x(self, i):
		return (i + 0.5) * self.d[0]
		
	def y(self, j):
		return (j + 0.5) * self.d[1]
	

	def reset_s(self):
		TW = self.T_boundary(-2)
		TE = self.T_boundary(2)
		TS = self.T_boundary(-3)
		TN = self.T_boundary(3)
		
		#print TW, TE, TS, TN
		
		
		
		dx = (self.ext[0,1] - self.ext[0,0]) / 2.0
		dy = (self.ext[1,1] - self.ext[1,0]) / 2.0
			
		T = self.mean_target
		
		#snew = ((T - TW)/dx + (T - TE)/dx + (T - TS)/dy + (T - TN)/dy) * k
		
		dSrc = k * (T - self.mean())

		self.Src += alpha_src * dSrc # / float(np.prod(self.n)) / 100000.0
		

		#print "Src =",self.Src
		
		#snew = snew / np.prod(self.n)
		
		#print "s_new =",snew
		
	def T_boundary(self, V):
		if V == -2:
			return np.mean(self.T[0,:])
		if V == 2:
			return np.mean(self.T[-1,:])
		if V == -3:
			return np.mean(self.T[:,0])
		if V == 3:
			return np.mean(self.T[:,-1])
		
		raise


	def nbr_to_loc(self, nbr):
		if not nbr:
			raise ValueError('nbr is None')
		
		if nbr == self.nbrs[0,0]:
			return -1
		if nbr == self.nbrs[0,1]:
			return 1
		if nbr == self.nbrs[1,0]:
			return -2
		if nbr == self.nbrs[1,1]:
			return 2
		
		
		print self.nbrsll, self.nbrsur
		print nbr

		raise ValueError('nbr not found')

	def loc_to_nbr(self, V):
		v,sv = v2is(V)
		return self.nbrs[v, (sv+1)/2]

	def index_lambda(self, nbr, par):
		PAR = self.glo_to_loc(par)
		
		ORT = self.nbr_to_loc(nbr)
		
		#print "PAR,ORT",PAR,ORT

		if PAR == 1:
			i = lambda p: p
			d = self.d[1]
		elif PAR == -1:
			i = lambda p: self.n[0] - p - 1
			d = self.d[1]
		else:
			if ORT < 0:
				i = lambda p: 0
			else:
				i = lambda p: self.n[0] - 1
		
		
		if PAR == 2:
			j = lambda p: p
			d = self.d[0]
		elif PAR == -2:
			j = lambda p: self.n[1] - p - 1
			d = self.d[0]
		else:
			if ORT < 0:
				j = lambda p: 0
			else:
				j = lambda p: self.n[1] - 1
		
		#print inspect.getsource(i)
		#print inspect.getsource(j)

		return i,j,d
		
	def term(self, ind, V, To):
		
		v,sv = v2is(V)
		
		isInterior = (ind[v] > 0 and sv < 0) or (ind[v] < (self.n[v] - 1) and sv > 0)
		
		if isInterior:
			a = 1.0 / self.d[v]

			indnbr = np.array(ind)
			indnbr[v] += sv

			T = self.T[indnbr[0],indnbr[1]]
		else:
			nbr = self.loc_to_nbr(V)
			if nbr:
				#print "neighbor face",V
				
				# local direction parallel to edge
				P = abs(cross(3, V))
				p,_ = v2is(P)

				li,lj,d = nbr.index_lambda(self, self.loc_to_glo(P))
				
				a = 2.0 / (self.d[v] + d)
				
				indnbr = [li(ind[p]), lj(ind[p])]
				
				T = nbr.T[indnbr[0],indnbr[1]]
			else:

				a = 1.0 / self.d[v]
				T = 2.0*self.T_bou[v,(sv+1)/2] - To
		
		return a,T
		
	def step(self):
		R = 0.0

		ver1 = False
		#ver1 = True

		ver2 = False

		for i in range(self.n[0]):
			for j in range(self.n[1]):
				To = self.T[i,j]

				aW, TW = self.term([i,j],-1, To)
				aE, TE = self.term([i,j], 1, To)
				aS, TS = self.term([i,j],-2, To)
				aN, TN = self.term([i,j], 2, To)
				
				"""
				if i > 0:
					aW = 1.0 / self.d[0]
					TW = self.T[i-1,j]
				elif self.nbrsll[0]:
					#print "west"

					nbr = self.nbrsll[0]
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(2))
					
					aW = 2.0 / (self.d[0] + d)
					TW = nbr.T[li(j),lj(j)]
				else:

					aW = 1.0 / self.d[0]
					TW = 2.0*self.Tll[0] - To


				if i < (self.n[0]-1):
					aE = 1.0 / self.d[0]
					TE = self.T[i+1,j]
				elif self.nbrsur[0]:
					#print "east"
					nbr = self.nbrsur[0]
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(2))
					
					aE = 2.0 / (self.d[0] + d)
					TE = nbr.T[li(j),lj(j)]
				else:
					aE = 1.0 / self.d[0]
					TE = 2.0*self.Tur[0] - To


				if j > 0:
					aS = 1.0 / self.d[1]
					TS = self.T[i,j-1]
				elif self.nbrsll[1]:
					
					
					nbr = self.nbrsll[1]
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(1))
					
					aS = 2.0 / (self.d[1] + d)
					TS = nbr.T[li(i),lj(i)]

					if ver1:
						print "south"
						print "aS =",aS,"TS =",TS,"To =",To
						ver2 = True
				else:
					aS = 1.0 / self.d[1]
					TS = 2.0*self.Tll[1] - To


				if j < (self.n[1]-1):
					aN = 1.0 / self.d[1]
					TN = self.T[i,j+1]
				elif self.nbrsur[1]:

					
					nbr = self.nbrsur[1]
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(1))
					
					aN = 2.0 / (self.d[1] + d)
					TN = nbr.T[li(i),lj(i)]

					if ver1:
						print "north"
						print "aN =",aN,"TN =",TN,"To =",To
						ver2 = True
				else:
					aN = 1.0 / self.d[1]
					TN = 2.0*self.Tur[1] - To
				"""
				
				#ver = True
			
				
				#print "source =",self.s(To)
				
				
				
				Ts = (aW*TW + aE*TE + aS*TS + aN*TN + self.s[i,j] * self.Src / k) / (aW + aE + aS + aN)

				dT = alpha * (Ts - To)

				if aW < 0 or aE < 0 or aS < 0 or aN < 0:
					print "aW aE aS aN"
					print aW, aE, aS, aN
					print "TW TE TS TN To Ts dT"
					print TW, TE, TS, TN, To, Ts, dT
					raise ValueError('bad')


				if ver1:
					print "aW aE aS aN"
					print aW, aE, aS, aN
					print "TW TE TS TN To Ts dT"
					print TW, TE, TS, TN, To, Ts, dT

				if math.isnan(To):
					raise ValueError('nan')
				if math.isnan(Ts) or math.isinf(Ts):
					print "aW aE aS aN"
					print aW, aE, aS, aN
					print "TW TE TS TN To Ts dT"
					print TW, TE, TS, TN, To, Ts, dT
					raise ValueError('bad')
				if math.isnan(dT):
					raise ValueError('nan')
				

				
				
			 
				self.T[i,j] += dT
				
				R += math.fabs(dT/To)
				
				if math.isnan(R):
					print dT, To
					raise ValueError('nan')
				
				
		return R

	def plot3(self, ax, T_max):
		x = [0]*3

		Xdir = abs(self.loc_to_glo(1)) - 1
		Ydir = abs(self.loc_to_glo(2)) - 1
		Zdir = abs(self.loc_to_glo(3)) - 1
		
		print "glo", Xdir, Ydir, Zdir
		
		x[Xdir] = np.linspace(self.ext[0,0],self.ext[0,1],self.n[0])
		x[Ydir] = np.linspace(self.ext[1,0],self.ext[1,1],self.n[1])
		
		print "x", x[Xdir]
		print "y", x[Ydir]
		
		x[Xdir],x[Ydir] = np.meshgrid(x[Xdir], x[Ydir])
		
		x[Zdir] = np.ones((self.n[0],self.n[1])) * self.z
		
		print np.shape(cm.jet(self.T))
		
		T = np.transpose(self.T)

		FC = cm.jet(T/T_max)

		ax.plot_surface(x[0], x[1], x[2], rstride=1, cstride=1, facecolors=FC, shade=False)
		
	def plot(self, V = None):
		fig = figure()
		ax = fig.add_subplot(121)
		
		self.plot_temp_sub(ax)
		
		# gradient
		ax = fig.add_subplot(122)

		self.plot_grad_sub(ax)
		
		return con
	def plot_temp_sub(self, ax, V = None):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])
		
		X,Y = np.meshgrid(x, y)
		
		T = np.transpose(self.T)
		
				
		if not V is None:
			con = ax.contourf(X, Y, T, V)
		else:
			con = ax.contourf(X, Y, T)
		
		pl.colorbar(con)
		pl.axis('equal')
		
	def plot_grad_sub(self, ax, V = None):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])
		
		X,Y = np.meshgrid(x, y)
		
		T = np.transpose(self.T)

		Z = np.gradient(T, self.d[0], self.d[1])
		Z = np.sqrt(np.sum(np.square(Z),0))
		
				
		if not V is None:
			con = ax.contourf(X, Y, Z, V)
		else:
			con = ax.contourf(X, Y, Z)
		
		pl.colorbar(con)
		pl.axis('equal')


	def plot_grad(self, V = None):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])
		
		X,Y = np.meshgrid(x, y)
		
		T = np.transpose(self.T)

		Z = np.gradient(T, self.d[0], self.d[1])
		Z = np.sqrt(np.sum(np.square(Z),0))
		
		
		#print np.shape(self.T)
		#print np.shape(Z)
		
		fig = figure()
		ax = fig.add_subplot(111)

		if not V is None:
			con = ax.contourf(X, Y, Z, V)
		else:
			con = ax.contourf(X, Y, Z)
		
		pl.colorbar(con)
		pl.axis('equal')

		return con

	def grad(self):
		return np.gradient(self.T, self.d[0], self.d[1])
	def grad_mag(self):
		return np.sqrt(np.sum(np.square(self.grad()),0))
	
	def temp_min(self):
		return np.min(self.T)
	def temp_max(self):
		return np.max(self.T)
	def grad_min(self):
		return np.min(self.grad_mag())
	def grad_max(self):
		return np.max(self.grad_mag())
	
	def mean(self):
		return np.mean(self.T)


def spreader_test():
	x = np.linspace(-1.,1.)
	y = np.linspace(-1.,1.)
	X,Y = np.meshgrid(x,y)
	
	Z = source_spreader(X,Y,1,1,2,2)

	con = pl.contourf(X,Y,Z)
	pl.colorbar(con)
	
	pl.show()
	

class Problem:
	def __init__(self, faces, name):
		self.faces = faces
		self.name = name

		signal.signal(signal.SIGINT, self)
		

	def __call__(self, signal, frame):
		print "saving"
		save_prob(self, self.name)
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
				R[-1] += face.step()
			
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
		cond2 = 1
		
		for it_3 in range(1000):
			it_2 = self.solve2(cond1_final, cond2, ver)
						
			if it_2 < it_cond and cond2 > cond2_final:
				cond2 /= 10**0.5


	def solve2(self, cond1_final, cond2, ver = False):
		cond1 = 1
		
		it_cond = 5

		R = 0.0
		for it_2 in range(it_max_2):
			
			it_1 = self.solve(cond1, ver, R)
			
			if it_1 < it_cond and cond1 > cond1_final:
				cond1 /= 10**1.0
			
			
			R = 0.0
			
			for f in self.faces:
				f.reset_s()
				R += math.fabs(f.mean() - f.mean_target) / f.mean_target
			
			print "{0:3d} {1:8e}".format(it_2,R)
			
			if math.isnan(R):
				raise ValueError('nan')
			
			if R < cond2:
				break
		
		return it_2

	def save(self, filename):
		f = open('case_' + filename, 'w')
		pickle.dump(self, f)


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
	




