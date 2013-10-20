import itertools
import sys
import math
import time
import os
import re
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('/nfs/stak/students/r/rymalc/Documents/python')

import read_csv
import interpolation2 as i2
import vector

tol = 1e-7



def nearest(x,X,n):
	print "nearest neighbor"
	n = np.prod(m)
	
	if 0:
		print np.shape(x)
	
	if np.ndim(x) != 1:
		raise Exception("x must be 1D array")
	if np.ndim(X) != 2:
		raise Exception("X must be 2D array")
	if np.ndim(i) != 1:
		raise Exception("i must be 1D array")
	
	d = np.size(x,0)
	p = np.size(X,0)
	
	if np.size(X,1) != d:
		raise Exception("size(X,1) must equal size(x,0)")
	if np.size(X,1) != d:
		raise Exception("size(X,1) must be greater than or equal to size(x,0)")
	
	# calculate distances
	r = np.zeros( p )
	for b in range(0,d):
		temp = np.power( ( X[:,b] - x[b] ), 2 )
		r += temp
	
	# sort
	ind = np.argsort( r )
	X = X[ind,:]
	
	return X[0:n,:]

def nearest_in_direction(x,X,n,dir):
	print "nearest neighbor"

	if np.ndim(dir) != 1:
		raise Exception("dir must be 1D array")
	if np.ndim(x) != 1:
		raise Exception("x must be 1D array")
	if np.ndim(X) != 2:
		raise Exception("X must be 2D array")
	
	d = np.size(x,0)
	p = np.size(X,0)
	
	if np.size(dir,0) != d:
		raise Exception("size(dir,0) must equal size(x,0)")
	if np.size(X,1) != d:
		raise Exception("size(X,1) must equal size(x,0)")
	if np.size(X,1) != d:
		raise Exception("size(X,1) must be greater than or equal to size(x,0)")
	
	dir = vector.norm( dir )
	
	Xnew = np.zeros((1,d))
	arg = np.array( [], int )
	
	for a in range(p):
		v = X[a,:] - x
		perp = np.dot( v, dir )	
		
		if perp > -tol:	
			v -= perp * dir
		
			if vector.magn( v ) < tol:
				#print np.shape(X[a,:])
				arg = np.append( arg, a )
				#Xnew = np.insert( Xnew, 1, X[a,:], axis=0 )
	
	#Xnew = np.delete( Xnew, 0, 0 )
	
	#X = Xnew
	#print np.shape(Xnew)

	m = np.size(arg,0)
	
	#print arg
	
	# calculate distances
	r = np.zeros( m )
	for b in range(d):
		temp = np.power( ( X[arg,b] - x[b] ), 2 )
		r += temp
	r = np.sqrt( r )
	
	# sort
	ind = np.argsort( r )
	
	r = r[ind]
	arg = arg[ind]
	
	return arg[0:n], r[0:n]
	

def dist_weigh_avg(x,X,Z):
	print "distance weighted average"
	
	if np.ndim(x) != 1:
		raise Exception("x must be 1D array")
	if np.ndim(X) != 2:
		raise Exception("X must be 2D array")
	if np.ndim(Z) != 1:
		raise Exception("Z must be 1D array")
	
	d = np.size(x,0)
	p = np.size(X,0)
	
	if np.size(X,1) != d:
		raise Exception("size(X,1) must equal size(x,0)")
	if np.size(Z,0) != p:
		raise Exception("size(Z,0) must equal size(X,0)")
	
	# calculate distances
	w = np.zeros( p )
	for b in range(0,d):
		temp = np.power( ( X[:,b] - x[b] ), 2 )
		w += temp

	W = np.sum(w)

	#print np.shape(w)
	#print np.shape(Z)
	#print W
	
	return np.sum( ( w * Z ) / W )
	
	
	
def matrix_prop(A):
	print A
	print "det =",np.linalg.det(A)
	print "eigvec"
	print np.linalg.eig(A)
	print "eigval =",np.linalg.eigvals(A)
	print "rank =",np.linalg.matrix_rank()
	

def nearest_neighbors(x,X,m,i,j):
	print "nearest neighbor"
	n = np.prod(m)
	
	if 0:
		print np.shape(x)
	
	if np.ndim(x) != 1:
		raise Exception("x must be 1D array")
	if np.ndim(X) != 2:
		raise Exception("X must be 2D array")
	if np.ndim(i) != 1:
		raise Exception("i must be 1D array")
	
	d = np.size(x,0)
	p = np.size(X,0)
	q = np.size(X,1)
	
	if np.size(i,0) != d:
		raise Exception("size(i,0) must equal size(x,0)")
	if q < d:
		raise Exception("size(X,1) must be greater than or equal to size(x,0)")
	
	
	#print "size(X,0)=",p
	
	# return array
	Y = np.zeros( (n,q) );
	
	R = np.zeros( n );
	R.fill(-1)
	
	# calculate distances
	r = np.zeros( p )
	for b in range(0,d):
		temp = np.power( ( X[:,i[b]] - x[b] ), 2 )
		r += temp
	
	
	s = np.argsort( r, axis=0 )
	#print "np.shape(s)",np.shape(s)
	
	
	
	u = np.zeros( (p,d) )
	u.fill(-1)
	
	ind = np.argsort( r )
	r = r[ind]
	X = X[ind,:]
	
	
	for b in range(0,d):
		e = 0
		for a in range(0,p):
			if u[a,b]==-1:
				u[ X[:,i[b]]==X[a,i[b]], b ] = e
				e += 1
	
	
	#print "u"
	#print u
	#print "m",m
	
	option = 1
	
	# first choice
	choices = np.zeros((1,n),int)
	#print np.shape(choices)
	choices[0,:] = np.arange(n)
	
	c = 0

	while 1:
		cc = np.size(choices,0)
		print "searching",cc,"choices"
		for a in range(cc):
			choice = choices[a,:]
			
			#print np.shape(X)
			#print choice
			#print i
			#print m
	
			A = i2.bicub_matrix( X[choice,:][:,i], m )
			Z = X[choice,j]
			
			B,inv = i2.numpy_invertible(A,Z)
		
			if inv:
				print "found!"
				return X[choice,:]
		
		# if that was the last set of choices
		if c == p:
			return None
		
		# next choice
		option += 1
		
		c = math.ceil( option * n )
		c = min(c,p)
		pool = range( c )
		#print "combinations ",( math.factorial(c) / math.factorial(n) / math.factorial(c-n) )
		choices = itertools.combinations( pool, n )
		choices = list( choices )
		
		#print "choices"
		#print choices
		
		choices = np.array( choices )
		
		#print "y"
		#print y
		
		# sort choices by sum of indices in radius array
		dist = np.sum( choices, axis=1 )
		ind = np.argsort( dist )
		print ind
		choices = choices[ind,:]


# sample grid
def grid_overlay(  ):
	nx = 10
	ny = 40

	x = np.linspace( -5e-4, 0, nx )
	y = np.linspace( -1e-3, 1e-3, ny )


	g = np.mgrid[0:nx,0:ny]

	#print "shape(g)=",np.shape(g)
	xv = x[ g[0] ]
	yv = y[ g[1] ]

	#print "shape(xv)=",np.shape(xv)

	z = np.zeros( np.shape(xv) )


	for a in range(0,np.size(x)):
		for b in range(0,np.size(y)):
		
			#Y = nearest_neighbors( np.array([x[a,b],y[a,b]]), data, m, i, j )
			
			#s = i2.spline( m, Y[:,[1,2]], Y[:,4] )
			
			#z[a,b] = s.eval_single( np.array([x[a,b],y[a,b]]) )
		
			Y = nearest( np.array([xv[a,b],yv[a,b]]), data[:,i], 4 )
			
			z[a,b] = dist_weigh_avg( np.array([xv[a,b],yv[a,b]]), data[:,i], data[:,j] )


	V = range(0,10000,20)
	plt.plot(np.ravel(xv),np.ravel(yv),'o')
	plt.plot(data[:,1],data[:,2],'s')
	CS = plt.contourf(xv,yv,z)
	CB = plt.colorbar(CS,shrink=0.8,extend='both')












