import math

import patch

class patch_group:
	def __init__(self, name, prob, v_0, S):
		
		self.patches = []

		self.prob = prob
		self.v_0 = v_0

		self.S = S

	def create_patch(self, name, normal, indices,
			T_bou = [[0,0],[0,0]]):
	
		#print 'T_0',T_0

		p = patch.Patch(self, name, normal, indices, 
				self.prob.x, self.prob.nx, self.prob.k, self.prob.alpha, self.prob.alpha_src,
				T_bou = T_bou)
		
		self.patches.append(p)
		
		return p

	def reset_s(self, equ_name):
		def debug():
			print "reset_s"
			print "equ_name",equ_name
			print equ.name
			print "v_m",v_m
			print "v_0",v_0
			print "dS",dS
			print "S",self.S[equ_name]
		
		v_0 = self.v_0[equ_name]
		
		if v_0 == 0.0:
			return
		
		# current area-weighted-average value
		v = float(0)
		A = float(0)
		
		for p in self.patches:
			for f in p.faces.flatten():
				equ = f.equs[equ_name]
		
				a = f.area()
				v += equ.mean() * a
				A += a
		
		v_m = v/A

		#equ = self.equs[equ_name]
		
		#vW = self.T_boundary(-2)
		#vE = self.T_boundary(2)
		#vS = self.T_boundary(-3)
		#vN = self.T_boundary(3)
		
		#dx = (self.ext[0,1] - self.ext[0,0]) / 2.0
		#dy = (self.ext[1,1] - self.ext[1,0]) / 2.0
		#A = dx * dy
		
		dv = v_0 - v_m
		
		dS = equ.k * dv / 10.
		
		self.S[equ_name] += dS
		
		#self.Tmean.append(vm)
		
		debug()
		
		return math.fabs(dv/v_0)

	def faces(self):
		for p in self.patches:
			for f in p.faces.flatten():
				yield f

	def write(self, equ_name):
		
		x = np.zeros(0)
		
		for f in self.faces():
			X,Y,Z = f.grid()
			
			x = np.append(x, X.ravel())
		
		name = self.name + '_prof_' + equ_name
		
		f = open(name + '.txt')
		
		f.write("(({0} point {1})",format(name,n))
		
		
		
		




