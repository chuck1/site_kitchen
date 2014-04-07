import numpy as np

class equation_prob:
	def __init__(self, prob, name, k, alpha, alpha_source):
		self.prob = prob
		self.name = name
		self.k = k
		self.alpha = alpha
		self.alpha_source = alpha_source

class Equ:
	# diffusion equation variable set

	def __init__(self, name, face, equ_prob):
		self.name = name
		self.face = face
		
		self.equ_prob = equ_prob

		#self.v_0 = v_0
		
		n_extended = self.face.n + np.array([2, 2])
		
		self.v = np.ones(n_extended) * self.face.patch.group.v_0[self.name]
		
		print "equation"
		print "name",self.name
		print "v_0",self.face.patch.group.v_0[self.name]

		self.s = np.ones(face.n)
		
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


