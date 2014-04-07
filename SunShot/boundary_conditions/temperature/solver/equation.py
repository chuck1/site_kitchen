import numpy as np


class Equ:
	# diffusion equation variable set

	def __init__(self, name, face, n, v_bou, k, al):
		self.name = name
		self.face = face
		
		self.n = n
		#self.v_0 = v_0
		
		n_extended = self.n + np.array([2, 2])
		
		self.v = np.ones(n_extended) * self.face.patch.group.v_0[self.name]
		
		self.v_bou = np.array(v_bou)
		
		if not np.shape(self.v_bou) == (2,2):
			print self.v_bou
			raise ValueError('')
		
		self.s = np.ones(n)
		
		self.k = k
		self.al = al
		
		self.flag = {"only_parallel_faces":False}
		
	def grad(self):
		return np.gradient(self.v[:-2,:-2], self.face.d[0,0,0], self.face.d[0,0,1])
	def grad_mag(self):
		return np.sqrt(np.sum(np.square(self.grad()),0))
	
	def min(self):
		return np.min(self.v[:-2,:-2])
	def max(self):
		v = np.max(self.v[:-2,:-2])
		print "v"
		print self.v
		print "max"
		print v
		return v
	def grad_min(self):
		return np.min(self.grad_mag()[:-2,:-2])
	def grad_max(self):
		return np.max(self.grad_mag()[:-2,:-2])
	
	def mean(self):
		return np.mean(self.v[:-2,:-2])


