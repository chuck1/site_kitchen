import time
import numpy as np
import itertools
from pylab import plot, show, figure, contour
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sympy import *
import math
import inspect
import pickle
import signal
import sys

k = 10

alpha = 1.4
alpha_src = 1.4

it_max_1 = 1000
it_max_2 = 1000


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

def save_prob(o, filename):
	f = open(filename, 'w')
	pickle.dump(o, f)
	
def load_prob(filename):
	f = open(filename, 'r')
	o = pickle.load(f)
	return o

def source_spreader(x,y,a,b,m,n):
	
	u = (1 - (x / a)**m) * (1 - (y / b)**n) * (m + 1) / m * (n + 1) / n
	
	return u


def forward(A):
	s = sign(A)
	a = abs(A - s)
	a = (((a+1) % 3) * s) + s
	return a
	
def backward(A):
	s = sign(A)
	a = abs(A - s)
	a = (((a+2) % 3) * s) + s
	return a
	
def next_dir(A):
	if A > 0:
		return forward(A)
	else:
		return backward(A)
def cross(a,b):
	#print a,b

	A = abs(a)-1
	B = abs(b)-1
	
	
	
	if B == (A+1) % 3:
		c = ((A+2) % 3) + 1
	else:
		c = ((A+1) % 3) + 1
		c = -c
	
	c *= sign(a) * sign(b)
	

	#print a, b, c

	return c

class Face:
	def __init__(self, N, ll, ur, z, n, Tll, Tur, mean_target):
		self.N = N
		
		self.ll = np.array(ll)
		self.ur = np.array(ur)
		self.z = z

		print "ll =",self.ll
		print "ur =",self.ur

		self.n = np.array(n)
		self.d = (self.ur - self.ll) / np.float32(self.n)
		self.T = np.ones(n) * mean_target
	
		self.Tur = np.array(Tur)
		self.Tll = np.array(Tll)

		self.nbrsll = [None,None]
		self.nbrsur = [None,None]

		self.S = 0
		self.s = np.zeros(n)
		
		
		self.mean_target = mean_target
		
		# source
		self.l = np.array([
			(self.ur[0] - self.ll[0]) / 2.0,
			(self.ur[1] - self.ll[1]) / 2.0])

		
		a = self.l[0] / 2.
		b = self.l[1] / 2.
		
		x = np.linspace(self.d[0] / 2. - a, a - self.d[0] / 2., self.n[0])
		y = np.linspace(self.d[1] / 2. - b, b - self.d[1] / 2., self.n[1])
		X,Y = np.meshgrid(x,y)
		
		self.s = source_spreader(X,Y,a,b,2,2)

		self.Src = 0

		# coordinates
		self.S = cross(self.N, abs(forward(self.N)))
		
		#print "f.S =",f.S

		self.R = cross(self.S, self.N)
	
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
		
		

		dx = (self.ur[0] - self.ll[0]) / 2.0
		dy = (self.ur[1] - self.ll[1]) / 2.0
			
		T = self.mean_target
		
		#snew = ((T - TW)/dx + (T - TE)/dx + (T - TS)/dy + (T - TN)/dy) * k
		
		dSrc = k * (T - self.mean())

		self.Src += alpha_src * dSrc # / float(np.prod(self.n)) / 100000.0
		

		#print "Src =",self.Src
		
		#snew = snew / np.prod(self.n)
		
		#print "s_new =",snew
		
	def T_boundary(self, v):
		if v == -2:
			return np.mean(self.T[0,:])
		if v == 2:
			return np.mean(self.T[-1,:])
		if v == -3:
			return np.mean(self.T[:,0])
		if v == 3:
			return np.mean(self.T[:,-1])

		raise
		

	def xyz_to_nrs(f, v):
		if v == -f.N:
			return -1
		if v == f.N:
			return 1

		if v == -f.R:
			return -2
		if v == f.R:
			return 2

		if v == -f.S:
			return -3
		if v == f.S:
			return 3
		
	def nrs_to_xyz(f, v):
		if v == 2:
			return f.R
		if v == -2:
			return -f.R
		if v == 3:
			return f.S
		if v == -3:
			return -f.S

		raise

	def nbr_to_nrs(self, nbr):
		if not nbr:
			raise ValueError('nbr is None')
		
		if nbr == self.nbrsll[0]:
			return -2
		if nbr == self.nbrsur[0]:
			return 2
		if nbr == self.nbrsll[1]:
			return -3
		if nbr == self.nbrsur[1]:
			return 3
		
		
		print self.nbrsll, self.nbrsur
		print nbr

		raise ValueError('nbr not found')

	def index_lambda(self, nbr, par):
		PAR = self.xyz_to_nrs(par)
		
		ORT = self.nbr_to_nrs(nbr)
		
		#print "PAR,ORT",PAR,ORT

		if PAR == 2:
			i = lambda p: p
			d = self.d[1]
		elif PAR == -2:
			i = lambda p: self.n[0] - p - 1
			d = self.d[1]
		else:
			if ORT < 0:
				i = lambda p: 0
			else:
				i = lambda p: self.n[0] - 1
		
		
		if PAR == 3:
			j = lambda p: p
			d = self.d[0]
		elif PAR == -3:
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
		
		
	def step(self):
		R = 0.0

		ver1 = False
		#ver1 = True

		ver2 = False

		for i in range(self.n[0]):
			for j in range(self.n[1]):
				To = self.T[i,j]

				if i > 0:
					aW = 1.0 / self.d[0]
					TW = self.T[i-1,j]
				elif self.nbrsll[0]:
					#print "west"

					nbr = self.nbrsll[0]
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(3))
					
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
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(3))
					
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
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(2))
					
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
					li,lj,d = nbr.index_lambda(self, self.nrs_to_xyz(2))
					
					aN = 2.0 / (self.d[1] + d)
					TN = nbr.T[li(i),lj(i)]

					if ver1:
						print "north"
						print "aN =",aN,"TN =",TN,"To =",To
						ver2 = True
				else:
					aN = 1.0 / self.d[1]
					TN = 2.0*self.Tur[1] - To
				
				
				#ver = True
			
				
				#print "source =",self.s(To)
				
				
				
				Ts = (aW*TW + aE*TE + aS*TS + aN*TN + self.s[i,j] * self.Src / k) / (aW + aE + aS + aN)

				dT = alpha * (Ts - To)



				if ver1:
					print "aW aE aS aN"
					print aW, aE, aS, aN
					print "TW TE TS TN To Ts dT"
					print TW, TE, TS, TN, To, Ts, dT

				if math.isnan(To):
					raise ValueError('nan')
				if math.isnan(Ts):
					raise ValueError('nan')
				if math.isnan(dT):
					raise ValueError('nan')
				

				
				
			
				self.T[i,j] += dT
				
				R += math.fabs(dT/To)
				
				if math.isnan(R):
					print dT, To
					raise ValueError('nan')
				
				
		return R

	def plot3d(self, V):
		x = [0]*3
		

		Xdir = Abs(self.xyz_to_nrs(1)) - 1
		Ydir = Abs(self.xyz_to_nrs(2)) - 1
		Zdir = Abs(self.xyz_to_nrs(3)) - 1
	
		print Xdir, Ydir, Zdir, x

		x[Xdir] = np.linspace(self.ll[0],self.ur[0],self.n[0])
		x[Ydir] = np.linspace(self.ll[1],self.ur[1],self.n[1])
		
		x[Xdir],x[Ydir] = np.meshgrid(x[Xdir], x[Ydir])
		
		x[Zdir] = np.ones((self.n[0],self.n[1])) * self.z
		
		
		print np.shape(cm.jet(self.T))
		
		FC = cm.jet(self.T)
		FC = np.ones(np.shape(self.T))

		fig = figure()
		
		ax = Axes3D(fig)
		
		ax.plot_surface(x[Xdir], x[Ydir], x[Zdir], rstride=1, cstride=1, facecolors=FC)
		
		#print type(X)
		#print np.shape(X)

		#Z = np.rot90(np.flip(self.T))
		#Z = self.T
		#Z = np.transpose(self.T)

		#con = pl.contourf(X,Y,Z, V)

		#pl.colorbar(con)

	def plot(self, V = None):
		ll = self.ll
		ur = self.ur
		
		x = np.linspace(ll[0],ur[0],self.n[0])
		y = np.linspace(ll[1],ur[1],self.n[1])
		
		X,Y = np.meshgrid(x, y)
		
		Z = np.transpose(self.T)
	
		fig = figure()
		ax = fig.add_subplot(111)
		
		if not V is None:
			con = ax.contourf(X, Y, Z, V)
		else:
			con = ax.contourf(X, Y, Z)
		
		pl.colorbar(con)
		pl.axis('equal')

		return con
	def plot_grad(self):
		ll = self.ll
		ur = self.ur
		
		x = np.linspace(ll[0],ur[0],self.n[0])
		y = np.linspace(ll[1],ur[1],self.n[1])
		
		X,Y = np.meshgrid(x, y)

		T = np.transpose(self.T)

		Z = np.gradient(T, self.d[0], self.d[1])
		Z = np.sqrt(np.sum(np.square(Z),0))
		
		
		#print np.shape(self.T)
		#print np.shape(Z)
		
		fig = figure()
		ax = fig.add_subplot(111)

		con = ax.contourf(X, Y, Z)
		
		pl.colorbar(con)
		
		return con

	def temp_min(self):
		return np.min(self.T)
	def temp_max(self):
		return np.max(self.T)
		
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

	def plot(self):
		a, b = nice_axes(self.temp_min(), self.temp_max())
		V = np.linspace(a, b, 21)
		
		for f in self.faces:
			f.plot(V)

		pl.show()
	
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
		
		#if ver:
			#pl.semilogy(R)
			#pl.show()
		
	
	def solve2(self, cond1, cond2, ver = False):
	
		R = 0.0
		for it in range(it_max_2):
				
			self.solve(cond1, ver, R)

			R = 0.0
			
			for f in self.faces:
				f.reset_s()
				R += math.fabs(f.mean() - f.mean_target) / f.mean_target
			
			print "{0:3d} {1:8e}".format(it,R)
			
			if math.isnan(R):
				raise ValueError('nan')

			if R < cond2:
				break
	






