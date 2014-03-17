import numpy as np

from unit_vec import *

def source_spreader(x,y,a,b,m,n):
	u = (1 - (x / a)**m) * (1 - (y / b)**n) * (m + 1) / m * (n + 1) / n
	return u


class Face(LocalCoor):
	def __init__(self, normal, ext, z, n, T_bou, mean_target, k):
		
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
		self.k = k

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
		
		dx = (self.ext[0,1] - self.ext[0,0]) / 2.0
		dy = (self.ext[1,1] - self.ext[1,0]) / 2.0
			
		T = self.mean_target
		
		dSrc = k * (T - self.mean()) * 10
		
		self.Src += alpha_src * dSrc
		
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
		
		print self.nbrs
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
				
				#ver = True
				#print "source =",self.s(To)
				
				Ts = (aW*TW + aE*TE + aS*TS + aN*TN + self.s[i,j] * self.Src / k) / (aW + aE + aS + aN)

				dT = alpha * (Ts - To)

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
		
		return
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


