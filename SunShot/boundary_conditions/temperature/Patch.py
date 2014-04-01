from Face import *
from Util import *

class Patch(LocalCoor):
	def __init__(self,
			normal, indices, x, nx, k, alpha, alpha_src,
			T_bou = [[0.,0.], [0.,0.]],
			T_tar = 30.0):
		
		LocalCoor.__init__(self, normal)
		
		print 'T_tar',T_tar

		self.k = k
		self.alpha = alpha
		
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
				
				pos_z = x[self.z][indices[self.z]]
				
				
				faces[i,j] = Face(
						normal, ext, pos_z, [numx, numy],
						T_bou, T_tar,
						k, alpha, alpha_src)
		
		self.npatch = np.array([NX,NY])

		self.faces = faces;

		self.grid_nbrs()
	
		
	def grid_nbrs(self):
		nx,ny = np.shape(self.faces)
	
		for i in range(nx):
			for j in range(ny):
				f1 = self.faces[i,j]
				if i > 0:
					if not f1.conns[0,0]:
						connect(f1, 0, 0, self.faces[i-1,j], 0, 1)
				if i < (nx-1):
					if not f1.conns[0,1]:
						connect(f1, 0, 1, self.faces[i+1,j], 0, 0)
				if j > 0:
					if not f1.conns[1,0]:
						connect(f1, 1, 0, self.faces[i,j-1], 1, 1)
				if j < (ny-1):
					if not f1.conns[1,1]:
						connect(f1, 1, 1, self.faces[i,j+1], 1, 0)

	


def stitch(patch1, patch2):
	if patch1 is None:
		return
	if patch2 is None:
		return

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

		f1 = patch1.faces[ind1[0],ind1[1]]
		f2 = patch2.faces[ind2[0],ind2[1]]

		#f1.nbrs[ol1,(sol1+1)/2] = f2
		#f2.nbrs[ol2,(sol2+1)/2] = f1

		connect(f1, ol1, (sol1+1)/2, f2, ol2, (sol2+1)/2)

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
		
		if not f1.conns[o,(sol1+1)/2] is None:
			print "face1", ind1
			print "face2", ind2
			raise ValueError('nbr not none')
		if not f2.conns[o,(sol2+1)/2] is None:
			raise ValueError('nbr not none')
		
		connect(f1, o, (sol1+1)/2, f2, o, (sol2+1)/2)
		#f1.nbrs[o,(sol1+1)/2] = f2
		#f2.nbrs[o,(sol2+1)/2] = f1
		
	


