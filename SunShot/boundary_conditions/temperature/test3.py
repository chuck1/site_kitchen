import numpy as np
import itertools
from pylab import plot, show, figure
from mpl_toolkits.mplot3d import Axes3D
from sympy import *


x, y, r, s, t, u, p, o = symbols('x y r s t u p o')

coor0 = [x, y]
coor1 = [r, s]
coor2 = [t, u]
coor = (x, y, r, s, t, u)

dp1, dp2, do1 = symbols('dp1, dp2, do1')

str = 'c_0:100'

C_all = list(symbols(str))

C1_all = list(symbols(str+'1'))
C2_all = list(symbols(str+'2'))




def combos(num):
	perm = list(itertools.product(range(num), repeat = 2))
	
	#print perm
	#print len(perm)
	
	stack = list(C_all)
	expr = 0
	for xpow, ypow in perm:
		expr += stack.pop(0) * x**xpow * y**ypow
	
	return expr


#pprint(func)
	

#
#
#
#
#func = a*x**2 + b*x + c

#func = a*x**2 + b*x + c*x**2*y + d*x*y + e*y + f


#func = a*x**3 + b*x**2 + c*x + d*x**3*y + e*x**2*y + f*x*y + g*y + h

#func = a*x**2 + b*x + c*x**2*y + d*x*y + e*y + f*x**2*y**2 + g*x*y**2 + h*y**2 + i


#func = C_all[0] * x**4 + C_all[1] * y**4 + C_all[2] * x**2 * y**2 + C_all[3] * x**2 + C_all[4] * y**2 + C_all[5]

func = combos(5)


#
#
#
#





pprint(func)





func1 = func
func2 = func
for s0,s1,s2 in zip(C_all + coor0, C1_all + coor1, C2_all + coor2):
	func1 = func1.subs(s0,s1)
	func2 = func2.subs(s0,s2)
	
#pprint(func1)
#pprint(func2)

C  = sorted([sym for sym in func.atoms(Symbol)  if sym not in coor], key=default_sort_key)
C1 = sorted([sym for sym in func1.atoms(Symbol) if sym not in coor], key=default_sort_key)
C2 = sorted([sym for sym in func2.atoms(Symbol) if sym not in coor], key=default_sort_key)

print "C =",C

coordinates = { 2  : r,
		-2 : -r,
		3  : s,
		-3 : -s}

coordinates_temp = {
		2  : t,
		-2 : -t,
		3  : u,
		-3 : -u}

def get_coor(v):
	if v == 2:
		return x
	if v == -2:
		return -x
	if v == 3:
		return y
	if v == -3:
		return -y


# row index in A
e = 0


def equ_equ(expr, x):

	#print "equ_equ"
	#print "\nexpr\n"
	#pprint(expr)
	temp = []
	if x in expr.atoms(Symbol):
		d = expr.diff(x)
		
		temp = equ_equ(d, x)
		
		expr = expr - Integral(d, x).doit()
		expr = expr.simplify()
		
		#pprint(expr)
		
	
	if expr != 0:
		temp.append(expr)
	else:
		print "zero expression"

	return temp

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


def set_nbrs(faces, i, nbrs):
	f = faces[i]
	f.nbrs = []
	for n in nbrs:
		if n == -1:
			f.nbrs.append([None])
		else:
			f.nbrs.append([faces[n]])


class Boundary:
	hello = 0
	
class Constant_Val(Boundary):
	def __init__(self, val):
		self.val = val
	
	def populate(self, f, ORT, A, B, row):
		
		PAR = cross(1, ORT)
		
		ort = get_coor(ORT)
		par = get_coor(PAR)
		
		par_sign = -1 if -1 in par.args else 1
		ort_sign = -1 if -1 in ort.args else 1
		
		expr = func - self.val
		
		#pprint(expr)

		expr = expr.subs(((ort_sign * ort, ort_sign * o), (par_sign * par, par_sign * p)))

		temp = equ_equ(expr, p)
		#for t in temp:
			#pprint(t)
		
		bou = f.nrs_to_bou(PAR)
		
		print "Constant generated {0} equations".format(len(temp))
		
		pprint(expr)
		for ex in temp:
			pprint(ex)
			ex = ex.subs(o, bou)
			
			f.pop_sub_sub2(ex, A, B, row)

			row += 1
		
		return A, B, row

class Constant_Slope(Boundary):
	def __init__(self, val):
		self.val = val
	
	def populate(self, f, ORT, A, B, row):
		
		PAR = cross(1, ORT)
		
		ort = get_coor(ORT)
		par = get_coor(PAR)
		
		par_sign = -1 if -1 in par.args else 1
		ort_sign = -1 if -1 in ort.args else 1
		
		expr = func
		
		#pprint(expr)

		expr = expr.subs(((ort_sign * ort, ort_sign * o), (par_sign * par, par_sign * p)))
		
		expr = expr.diff(p) - self.val

		temp = equ_equ(expr, p)
		#for t in temp:
			#pprint(t)
		
		bou = f.nrs_to_bou(PAR)
		
		print "Constant generated {0} equations".format(len(temp))
		
		#pprint(expr)
		for ex in temp:
			#pprint(ex)
			ex = ex.subs(o, bou)
			
			f.pop_sub_sub2(ex, A, B, row)

			row += 1
		
		return A, B, row



class face:
	def __init__(f, i, N, r0, r1, s0, s1, int_val):
		f.i = i
		f.N = N
		f.r0 = r0
		f.r1 = r1
		f.s0 = s0
		f.s1 = s1
		f.int_val = int_val

		f.dr = r1 - r0
		f.ds = s1 - s0

		#print "f.n =",f.N

		f.S = cross(f.N, abs(forward(f.N)))
		
		#print "f.S =",f.S

		f.R = cross(f.S, f.N)
		

	def populate(f, A, B, e):
		#f.pop_r_bou(A)	
		#f.pop_s_bou(A)
		
		# boundaries
		for p in [1, 2, 3]:
			if p != abs(f.N):
				print "face boundary"
				A, B, e = f.pop_bou(A, B, e, p)
		
		for PAR in [-2, 2, -3, 3]:
			print "check for boundary at ",PAR
			nbrs = f.nrs_to_nbr(PAR)
			for nbr in nbrs:
				if isinstance(nbr, Boundary):
					A, B, e = nbr.populate(f, PAR, A, B, e)
		
		# integral
		A, B, e = f.pop_int(A, B, e)
		
		# set coefficiencts to zero
		#A, B = f.pop_sub_sub(A, B, e, C1_all[4] - 0, f, None)
		#e += 1
		#A, B = f.pop_sub_sub(A, B, e, C1_all[7] - 0, f, None)
		#e += 1

		
		
		return A, B, e

	def pop_int(f, A, B, e):
		
		expr = integrate(func, (x, 0, f.dr), (y, 0, f.ds)) - f.int_val
		
		A, B = f.pop_sub_sub2(expr, A, B, e)
		e += 1
		
		return A, B, e

	def delta(f, A):
		options = {
				2 : f.dr,
				3 : f.ds}
		return options[abs(A)]

	def xyz_to_nrs(f, v):
		options = {
				f.N  : 1,
				-f.N : -1,
				f.R  : 2,
				-f.R : -2,
				f.S  : 3,
				-f.S : -3}
		
		if v == f.S:
			return 3

		#print "v =",v
		#print "NRS =",f.N, f.R, f.S
		#print options
		#print options[3]
		return options[v]
		
	def nrs_of_nbr(f, nbr):
		options = {
			0: -2,
			1: 2,
			2: -3,
			3: 3}
	
		for ind in range(4):
			if nbr in f.nbrs[ind]:
				return options[ind]
		
		
		
		
	def nrs_to_bou(f, E):
		if E == -2:
			return 0
		if E == 2:
			return f.dr
		if E == -3:
			return 0
		if E == 3:
			return f.ds

		

	def nrs_to_nbr(f, E):
		options = {
				-2 : 0,
				2  : 1,
				-3 : 2,
				3  : 3}

		return f.nbrs[options[E]]
		
	def pop_bou(f, matrix, B, e, ort):
		
		# par    xyz of nbr
		par = cross(ort,f.N)
		
		# PAR1   nrs of nbr
		PAR1 = f.xyz_to_nrs(par)
		
		# nbr
		nbr = f.nrs_to_nbr(PAR1)[0]
		
		
		if not isinstance(nbr, face):
			print "not face"
			return A, B, e
		
		PAR2 = nbr.nrs_of_nbr(f)
		
		#b = -1 * sign(E1) * sign(E2)
		

		par_disp = 0

		if PAR2 > 0:
			par_disp += dp2

		if PAR1 > 0:
			par_disp += dp1
		
		#par_disp += 

		#d *= sign(E1) * sign(E1)
		
		par1 = coordinates[PAR1]
		par2 = coordinates_temp[PAR2]
		
		# d      displacement
		# b      + or -
		# par1   r or s
		# par2   t or u
		
		
		
		ORT1 = f.xyz_to_nrs(ort)
		ORT2 = nbr.xyz_to_nrs(ort)
		
		ort1 = coordinates[ORT1]
		ort2 = coordinates_temp[ORT2]
		
		ort_disp = 0
		
		if sign(ORT1) != sign(ORT2):
			ort_disp = do1
		
		f2 = func2
		
		#print par2, ort2
		s = sign(lambdify(t,par2)(1))
		
		s_par2 = -1 if -1 in par2.args else 1
		s_ort1 = -1 if -1 in ort1.args else 1
		
		# substitute temporary coordinates with face 1 coordinates
		f2 = f2.subs(s * par2, s * (par_disp - par1))
		f2 = f2.subs(ort2, ort1 - ort_disp)
	
		g = func1 - f2

		#print "\ng\n"
		#pprint(g)

		# substitue face 1 coordinates with po coordinates
		g = g.subs(((par1, p), (ort1, o)))
		
		gp = g.diff(p)
		
		
		#ort1_pos = ort1 * s_ort1
		
		# value
		temp = equ_equ(g, o)
		
		# first derivative
		temp += equ_equ(gp, o)
		
		#temp += equ_equ(g.diff(p).diff(p), o)

		#pprint(temp)
		
		bou = f.nrs_to_bou(PAR1)

		DP1 = f.delta(PAR1)
		DP2 = nbr.delta(PAR2)
		DO1 = f.delta(ORT1)
		
		print "Face Boundary generated {0} equations".format(len(temp))
		
		matrix, B, e = f.pop_sub(matrix, B, e, temp, nbr, bou, DP1, DP2, DO1)
		
		ver = False
		if ver:
			print "PAR1 =",PAR1
			print "PAR2 =",PAR2
			print "ORT1 =",ORT1
			print "ORT2 =",ORT2
			print "par_disp =",par_disp
			print "ort_disp =",ort_disp

			print s * par2, "=", s * (par_disp - par1)
			print ort2, "=", ort1 - ort_disp
			
			print "bou =", bou
			
			print "\ng\n"
			pprint(g)
			print "\ngp\n"
			pprint(gp)

		return matrix, B, e
		

	def pop_sub(f, A, B, e, temp, nbr, bou, DP1, DP2, DO1):
		for expr in temp:

			#pprint(expr)
			expr = expr.subs(((p, bou), (dp1, DP1), (dp2, DP2), (do1, DO1)))
			#pprint(expr)
			
			A, B = f.pop_sub_sub(A, B, e, expr, f, nbr)
			e += 1
		
		return A, B, e
		
	def pop_sub_sub(f, A, B, e, expr, face1, face2):

		#print "\npop_sub_sub expr\n"
		#pprint(expr)
		
		col = face1.i * order
		for co in C1:
			v = expr.coeff(co)
			
			A[e,col] = v
			
			col += 1
			
			expr -= v*co

		if face2:
			col = face2.i * order
			for co in C2:
				v = expr.coeff(co)

				A[e,col] = v
			
				col += 1

				expr -= v*co

		

		#pprint(expr)
		
		B[e] = -expr
		
		return A, B

	def pop_sub_sub2(self, expr, A, B, row):
		#print "\npop_sub_sub expr\n"
		#pprint(expr)
		
		col = self.i * order
		for co in C:
			v = expr.coeff(co)
			
			#print row,col
			A[row,col] = v
			col += 1
			expr -= v*co
			#print co,v
		
		
		#pprint(expr)		
		B[row] = -expr
		
		return A, B

	def plot(f, ax, C):
		g = func1

		col = f.i * order
		for co in C1:
			g = g.subs(co, C[col])
			col += 1
		
		l = lambdify((r, s), g)
		
		x = np.linspace(f.r0, f.r1)
		y = np.linspace(f.s0, f.s1)
		
		X,Y = np.meshgrid(x,y)
		Z = l(X - f.r0, Y - f.s0)
		
		ax.plot_surface(X,Y,Z, rstride=20, cstride=1)

		#for i in range(len(x)):
		#	for j in range(len(y)):
		#		z[i,j] = l(x[i],y[j])
		
		
		
		
# number of coefficiencts
order = len(C)



"""
faces = []

f = face(0, 1, 0, 1, 0, 1, 10)

#f.nbrs = [[Constant_Val(0), Constant_Slope(0)], [Constant_Val(0)], [Constant_Val(0)], [Constant_Val(0)]]
#f.nbrs = [[Constant_Val(0)], [Constant_Val(0)], [Constant_Val(0)], [Constant_Val(0)]]

faces.append(f)

n = len(faces)
"""

faces = []
n = 3
for ind in range(n):
	faces.append(face(ind, 1, ind, ind + 1, 0, 1, ind*10))

for ind in range(n):
	ind0 = ind - 1 if ind > 0 else n-1-ind
	ind1 = ind + 1 if ind < (n-1) else ind-n+1

	set_nbrs(faces, ind, [ind0, ind1, -1, -1])



print "num of faces =",n
print "num of coeff =",order



A = np.zeros((n * order,n * order))
B = np.zeros((n * order))

for f in faces:
	A, B, e = f.populate(A, B, e)

#print A
#print B
print e, n*order

print "det(A) =",np.linalg.det(A)

C = np.linalg.solve(A,B)



should_plot = True

if should_plot:
	fig = figure()
	ax = Axes3D(fig)

	for f in faces:
		f.plot(ax, C)

	show()




















