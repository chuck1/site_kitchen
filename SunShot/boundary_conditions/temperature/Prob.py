import time
import numpy as np
import itertools
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import math
import inspect
import pickle
import signal
import sys

from Face import *
from Patch import *

class Problem:
	def __init__(self, name, x, nx, k, alpha, alpha_src,
			it_max_1 = 100, it_max_2 = 100):
		self.name = name
		
		self.x = x
		self.nx = nx

		self.k = k
		
		self.alpha = alpha
		self.alpha_src = alpha_src

		self.it_max_1 = it_max_1
		self.it_max_2 = it_max_2

		self.faces = []
		signal.signal(signal.SIGINT, self)

	def createPatch(self, normal, indices,
			T_bou = [[0,0],[0,0]],
			T_tar = 1.0):
	
		print 'T_tar',T_tar

		p = Patch(normal, indices, self.x, self.nx, self.k, self.alpha, self.alpha_src,
				T_bou = T_bou, T_tar = T_tar)
		
		self.faces += list(p.faces.flatten())
		return p
	def __call__(self, signal, frame):
		print "saving"
		#self.save()
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
			f.plot(V, Vg)
			#f.plot_grad(Vg)
		
		pl.show()
	def get_3d_axes(self):
		x = self.x

		x_mean = np.zeros(3)
		x_min = np.zeros(3)
		x_max = np.zeros(3)
		
		for a in range(3):
			x_mean[a] = np.mean(x[a])
			x_min[a] = min(x[a])
			x_max[a] = max(x[a])
			
		
		x_rng = x_max - x_min
		
		x_rng_max = max(x_rng) * 0.5
		
		#print x_mean
		#print x_rng
		#print x_rng_max
		
		l = x_mean - x_rng_max
		u = x_mean + x_rng_max
		
		return l,u

	def plot3(self):
		T_max = self.temp_max()
		
		fig = pl.figure()
		ax = Axes3D(fig)
		


		for f in self.faces:
			f.plot3(ax, T_max)
		
		l,u = self.get_3d_axes()
		
		ax.set_xlim3d(l[0], u[0])
		ax.set_ylim3d(l[1], u[1])
		ax.set_zlim3d(l[2], u[2])

		return ax
	
	def solve(self, cond, ver=True, R_outer=0.0):
		return self.solve_serial(cond, ver, R_outer)

	def solve_serial(self, cond, ver=True, R_outer=0.0):
		
		R = np.array([])
	
		for it in range(self.it_max_1):
			R = np.append(R, 0.0)
			
			for face in self.faces:
				R[-1] = max(face.step(), R[-1])
				face.send()
			
			for face in self.faces:
				face.recv()
			
			
			if ver:
				print "{0:3d} {1:8e} {2:8e}".format(it, R_outer, R[-1])
			
			if math.isnan(R[-1]):
				raise ValueError('nan')
			
			if R[-1] < cond:
				break
		
		return it
		

	def solve2(self, cond1_final, cond2, ver = False):
		#cond1 = 1
		
		#it_cond = 2
		
		R = 1.0
		for it_2 in range(self.it_max_2):
			
			cond1 = R / 10.0 # target residual for inner loop is proportional to current residual for outer loop
			
			it_1 = self.solve(cond1, ver, R)
			
			R = 0.0
			
			for f in self.faces:
				Rn = f.reset_s()
				
				R = max(Rn, R)
			
			print "{0:3d} {1:8e}".format(it_2,R)
			
			if math.isnan(R):
				raise ValueError('nan')
			
			if R < cond2:
				break
		
		return it_2

	def save(self):
		f = open('case_' + self.name, 'w')
		pickle.dump(self, f)



