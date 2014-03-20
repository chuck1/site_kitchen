import math
import numpy as np
import multiprocessing
from matplotlib import cm
import pylab as pl

from unit_vec import *

def source_spreader(x,y,a,b,m,n):
	u = (1 - np.power(x / a, m)) * (1 - np.power(y / b, n)) * (m + 1) / m * (n + 1) / n
	return u

class Conn:
	# information concerning connection between face and nbr
	# from perspective of face
	def __init__(self, face, conn):
		self.face = face
		self.conn = conn
		
		self.MP = False

	def refresh(self):
		self.OL = self.face.nbr_to_loc(self.twin.face)
		
		self.ol, self.sol = v2is(self.OL)
		
		self.PL = abs(cross(3, self.OL))
		self.pl,_ = v2is(self.PL)

		self.PG = self.face.loc_to_glo(self.PL)
		
		self.li, self.lj, self.d = self.face.index_lambda(self.twin.face, self.PG)
		
	def send(self, T):
		if self.MP:
			self.conn.send(T)
		else:
			self.T = T
	
	def recv(self):
		
		if self.MP:
			T = self.conn.recv()
		else:
			T = self.twin.T
		
		return T

class Face(LocalCoor):
	def __init__(self, normal, ext, z, n, T_bou, mean_target, k, alpha, alpha_src):
		
		self.ext = np.array(ext)
		
		self.z = z
		
		self.n = np.array(n)

		# the extra 2 rows/cols are for storing neighbor values
		n_extended = self.n + np.array([2, 2])
		
		
		self.d = np.zeros((n_extended[0], n_extended[1], 2))
		for i in range(n_extended[0]):
			for j in range(n_extended[1]):
				self.d[i,j,:] = (self.ext[:,1] - self.ext[:,0]) / np.float32(self.n)

		
		# temperature array
		self.T = np.ones(n_extended) * mean_target
		
		if np.any(self.d < 0):
			print self.d
			raise ValueError('bad')
		
		self.T_bou = np.array(T_bou)

		self.conns = np.empty((2,2), dtype=object)
		
		
		self.S = 0
		self.s = np.zeros(n)
		
		
		self.mean_target = mean_target
		self.k = k
		self.alpha = alpha
		self.alpha_src = alpha_src

		# source
		self.l = np.array([
			(self.ext[0,1] - self.ext[0,0]) / 2.0,
			(self.ext[1,1] - self.ext[1,0]) / 2.0])
		
		
		a = self.l[0] / 2.
		b = self.l[1] / 2.
		
		x = np.linspace(self.d[0,0,0] / 2. - a, a - self.d[0,0,0] / 2., self.n[0])
		y = np.linspace(self.d[0,0,1] / 2. - b, b - self.d[0,0,1] / 2., self.n[1])
		Y,X = np.meshgrid(y,x)
		
		self.s = source_spreader(X,Y,a,b,2,2)

		self.Src = 0

		# coordinates
		LocalCoor.__init__(self, normal)

		self.Tmean = []

	def x(self, i):
		return (i + 0.5) * self.d[0]
		
	def y(self, j):
		return (j + 0.5) * self.d[1]
	

	def reset_s(self):
		TW = self.T_boundary(-2)
		TE = self.T_boundary(2)
		TS = self.T_boundary(-3)
		TN = self.T_boundary(3)
		
		dx = (self.ext[0,1] - self.ext[0,0]) / 2.0
		dy = (self.ext[1,1] - self.ext[1,0]) / 2.0
			
		Tm = self.mean()

		dT = self.mean_target - Tm
		
		dSrc = self.k * dT / 1000.
		
		self.Src += self.alpha_src * dSrc
		
		self.Tmean.append(Tm)
		
		return math.fabs(dT/self.mean_target)

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
		if not isinstance(nbr, Face):
			raise ValueError('nbr is not Face')
		if not nbr:
			raise ValueError('nbr is None')
		
		for i in range(2):
			for j in range(2):
				conn = self.conns[i,j]
				if conn:
					if nbr == conn.twin.face:
						return is2v(i,2*j-1)
		
		print [conn.nbr if conn else conn for conn in self.conns.flatten()]
		print nbr
		raise ValueError('nbr not found')

	def loc_to_conn(self, V):
		v,sv = v2is(V)
		return self.conns[v, (sv+1)/2]

	def index_lambda(self, nbr, par):
		# returns lambda which is function of positive parallel index of neighbor
		# and return for index of my cell
		
		if not isinstance(nbr, Face):
			raise ValueError('nbr is not a Face')
		
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
	
	def send_array(self, conn):
		T = np.ones(self.n[conn.pl])
		
		for a in range(self.n[conn.pl]):
			T[a] = self.T[conn.li(a), conn.lj(a)]
		
		conn.send(T)
		
	def recv_array(self, conn):
		T = conn.recv()
		
		ind = [0,0]
		ind[conn.ol] = -1 if conn.sol < 1 else self.n[conn.ol]
		
		for a in range(self.n[conn.pl]):
			ind[conn.pl] = a
			
			self.T[ind[0],ind[1]] = T[a]
		
	def term(self, ind, V, To):
		
		v,sv = v2is(V)
		
		isInterior = (ind[v] > 0 and sv < 0) or (ind[v] < (self.n[v] - 1) and sv > 0)
		
		conn = self.loc_to_conn(V)
		d = self.d[ind[0],ind[1],v]

		if isInterior or ((not isInterior) and conn):
			# interior cells and boundary cells with Face neighbors
			indnbr = np.array(ind)
			indnbr[v] += sv
			
			T = self.T[indnbr[0],indnbr[1]]

			#print ind,indnbr
			#print "T",T,"To",To
			
			d_nbr = self.d[indnbr[0],indnbr[1],v]
			
			a = 2.0 / (d + d_nbr)
		else:
			#print "boundary"

			a = 1.0 / d
			T = 2.0*self.T_bou[v,(sv+1)/2] - To
			"""
			if conn:
				#print "neighbor face",V
				
				# local direction parallel to edge
				P = abs(cross(3, V))
				p,_ = v2is(P)
				
				li,lj,d = conn.twin.face.index_lambda(conn.face, self.loc_to_glo(P))
				
				a = 2.0 / (self.d[v] + d)
				
				indnbr = [li(ind[p]), lj(ind[p])]
				
				T = conn.twin.face.T[indnbr[0],indnbr[1]]
			else:
			"""
					

		return a,T
	

	def step(self):
		R = 0.0
		
		ver1 = False
		#ver1 = True
		
		ver2 = False
		
		# solve equation

		for i in range(self.n[0]):
			for j in range(self.n[1]):
				To = self.T[i,j]

				aW, TW = self.term([i,j],-1, To)
				aE, TE = self.term([i,j], 1, To)
				aS, TS = self.term([i,j],-2, To)
				aN, TN = self.term([i,j], 2, To)
				
				#ver = True
				#print "source =",self.s(To)
				
				Ts = (aW*TW + aE*TE + aS*TS + aN*TN + self.s[i,j] * self.Src / self.k) / (aW + aE + aS + aN)

				dT = self.alpha * (Ts - To)

				def debug():
					print "aW aE aS aN"
					print aW, aE, aS, aN
					print "TW TE TS TN To Ts dT"
					print TW, TE, TS, TN, To, Ts, dT
				
				
				if aW < 0 or aE < 0 or aS < 0 or aN < 0:
					debug()
					raise ValueError('bad')

				if ver1: debug()

				if math.isnan(To):
					raise ValueError('nan')
				if math.isnan(Ts) or math.isinf(Ts):
					debug()
					raise ValueError('bad')
				if math.isnan(dT):
					raise ValueError('nan')
			 
				self.T[i,j] += dT
				
				R = max(math.fabs(dT/To), R)
				
				if math.isnan(R):
					print dT, To
					raise ValueError('nan')
		return R

	def send(self):
		# send/recv neighbor values
		for con in self.conns.flatten():
			if con:
				self.send_array(con)
	
	def recv(self):
		for con in self.conns.flatten():
			if con:
				self.recv_array(con)	
		
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
		
		x[Ydir],x[Xdir] = np.meshgrid(x[Ydir], x[Xdir])
		
		x[Zdir] = np.ones((self.n[0],self.n[1])) * self.z
	
		
				
		T = np.transpose(self.T[:-2,:-2])

		FC = cm.jet(T/T_max)

		print np.shape(x[0])
		print np.shape(x[1])
		print np.shape(x[2])
		print np.shape(FC)

		ax.plot_surface(x[0], x[1], x[2], rstride=1, cstride=1, facecolors=FC, shade=False)
		
	def plot(self, V = None, Vg = None):
		fig = pl.figure()
		ax = fig.add_subplot(121)
		
		self.plot_temp_sub(ax, V)
		
		# gradient
		ax = fig.add_subplot(122)
		
		self.plot_grad_sub(ax, Vg)
		
		return
	def plot_temp_sub(self, ax, V = None):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])
		
		X,Y = np.meshgrid(x, y)
		
		T = np.transpose(self.T[:-2,:-2])
		
		print np.shape(X)
		print np.shape(Y)
		print np.shape(T)
		
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
		
		Z = self.grad_mag()
		Z = Z[:-2,:-2]
		
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
		return np.gradient(self.T, self.d[0,0,0], self.d[0,0,1])
	def grad_mag(self):
		return np.sqrt(np.sum(np.square(self.grad()),0))
	
	def temp_min(self):
		return np.min(self.T[:-2,:-2])
	def temp_max(self):
		return np.max(self.T[:-2,:-2])
	def grad_min(self):
		return np.min(self.grad_mag()[:-2,:-2])
	def grad_max(self):
		return np.max(self.grad_mag()[:-2,:-2])
	
	def mean(self):
		return np.mean(self.T[:-2,:-2])

def connect(f1, a1, b1, f2, a2, b2, multi = False):
	if multi:
		c1, c2 = multiprocessing.Pipe()
	else:
		c1, c2 = None, None
	
	conn1 = Conn(f1, c1)
	conn2 = Conn(f2, c2)
	
	conn1.twin = conn2
	conn2.twin = conn1
	
	#f1.nbrs[a1,b1] = f2
	#f2.nbrs[a2,b2] = f1
	
	f1.conns[a1,b1] = conn1
	f2.conns[a2,b2] = conn2
	
	conn1.refresh()
	conn2.refresh()

