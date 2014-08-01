#!/usr/bin/env python

import sys, os
import numpy as np
import math
import scipy.optimize

module_dir = os.environ["HOME"] + "/Documents/Programming/Python/Modules/"
sys.path.append(module_dir)

import csv

import argparse


# a*(x*x + y*y) + b*(x + y) + c

def fun1(p, x, y, x0 = 0.0, y0 = 0.0):
        return p[0] * np.exp(p[1] * (x**2 + y**2))


# centered normal distribution
	

# non-centered normal distribution
def fun2(p, x):
	return p[0] * np.exp(p[1] * (x - p[2])**2)

def errfun2(p, r, f):
	return f - fun2(p, r)


# centered normal distribution
def fun3(p, r):
	return p[0] * np.exp(p[1] * r**2)

def fun3xy(p, x, y, x0 = 0.0, y0 = 0.0):
	r = np.sqrt(np.square(x - x0) + np.square(y - y0))
	return fun3(p, r)



def fun_grid(p, fun, x, y, n, xm = 0.0, ym = 0.0):
	x = np.linspace(x[0], x[1], n)
	y = np.linspace(y[0], y[1], n)
	
	#print x
	#print y

	X,Y = np.meshgrid(x,y)
	
	F = fun(p,X,Y,xm,ym)
	
	return X,Y,F
	
def numerically_integrate_2D(p,fun, x, y):
	# equation:
	# f = a * exp(b * x**2)
	# a and b are constants
	# x is distance from center
	
	res = 0.01
	
	n = 100
	
	l = x[1] - x[0]
	w = y[1] - y[0]

	A = l * w
	
	A_cell = (l/float(n-1)) * (w/float(n-1))
	
	X,Y,F = fun_grid(p, fun, x, y, n)

	FA = F * A_cell
	
	def plot():
		CS = plt.contourf(X,Y,F)
		CB = plt.colorbar(CS,format='%e')
		CB.set_label('heat flux (W/m2)')
		plt.axis('equal')
		plt.show()
	
	#plot()
	
	aa = np.sum(FA) / A
	#print "area average = {0:e}".format(aa)
	return aa
	
def fun(x,a,b):
	y = a*x*x + b
	return y

def integrate_poly2d(w, p):
	o = np.size(p,0)
	
	n = np.arange(o)[::-1]
	
	w = np.ones(o) * w
	
	print
	print
	
	z = 2 * p / (n+1) * np.power(w,n+2) 

	print p
	print n
	print w
	print z

	z = np.sum(z)
	
	print z
	
	# int 0 w int 0 w    a * (x^n) * dx * dy
	
	# 2 * a / (n+1) * w^(n+1) * w
	# 2 * a / (n+1) * w^(n+2)
	
	# n = 0
	# 2 * a * w^2
	
        return z

def scale( S, w, p):
	S0 = integrate_poly2d(w, p)
	
	
	
	c = ( S - S0 ) / w / w / 2
	
        return c
	
def parab_2d_coeff_from_meas( peak, edge, edge_x ):
	a = ( edge - peak ) / edge_x / edge_x
	
        return a

def plot2d(filename,a,c):
	
	data = np.zeros((40,2))
	
	r = 0
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data[r,0] = float(row[0]) * 0.001
			data[r,1] = float(row[1]) * 10000
			r += 1
	
	print np.shape(data)
	print data
	
	x = data[0:15,0] - 0.005
	y = data[0:15,1]
	
	plt.plot(x,y,'o')
	
	x = data[15:30,0] - 0.005
	y = data[15:30,1]
	
	plt.plot(x,y,'s')
	
	plt.plot(x,fun(x,a,c))

	plt.xlabel('x (m)')
	plt.ylabel('heat flux (W/m2)')
	
	plt.show()
	
def get_csv_data(filename):
	raw = []
	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile) 
		for row in spamreader:
			raw.append(list(float(c) for c in row))
	
	data = np.array(raw)
	
	return data

#=================================================================================================
#=================================================================================================
#=================================================================================================

def convert_arg_line_to_args(self, arg_line):
	for arg in arg_line.split():
		if not arg.strip():
			continue
		yield arg

class Action(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if not getattr(namespace, 's'):
			parser.error("requires -s")
		else:
			setattr(namespace,self.dest,values)


if __name__=='__main__':
	
	parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
	parser.add_argument('-p', action="store_true")
	parser.add_argument('-s', type=float, help='half-width of heated surface')
	parser.add_argument('-f', type=float)
	parser.add_argument('--prof', action=Action, help='write profile file')
	parser.add_argument('-x', type=float, help='x origin for profile file')
	parser.add_argument('-y', type=float, help='y origin for profile file')
	parser.add_argument('-z', type=float, help='z origin for profile file')
	parser.add_argument('filename', help='csv file')
	args = parser.parse_args()
	
	
	data = get_csv_data(args.filename)

	# extract x and y
	x = data[:,0]
	y = data[:,1]
	
	# correct units
	x = x * 1e-3
	y = y * 1e4
	
	x_sort = np.sort(x)

	p,_ = scipy.optimize.leastsq(errfun2, [1.0e6, -1.0e3, 0.0], args=(x, y))
	

	print "{0:16}{1}".format("p", p)

	
	


	if args.f and args.s:

		print "{0:16}{1: e}".format("flux", args.f)
		
		f_int_1 = numerically_integrate_2D(p, fun3xy, [0.0, args.s], [0.0, args.s])
		
		p2 = np.array(p)
		p2[0] = p2[0] * args.f / f_int_1
		
		print "{0:16}{1}".format("p scaled", p)
		
		f_int_2 = numerically_integrate_2D(p, fun3xy, [0.0, args.s], [0.0, args.s])
		
	
	if args.p:
		import pylab as pl

		leg = []
		
		pl.plot(x,y,'o')
		leg.append('experimental')
		
		pl.plot(x_sort,fun2(p,x_sort))
		leg.append('normal dist')
	
		if args.f and args.s:
			pl.plot(x_sort,fun2(p2,x_sort))
			leg.append('normal dist scaled')
		

		pl.xlabel('position (m)')
		pl.ylabel('heat flux (W/m2)')
		pl.legend(leg, loc='lower center')
		pl.show()
	
		

	if args.prof:
		import fluent
		
		xe = np.array([0, args.s * 2.0])
		xe += args.x
		
		ze = np.array([0, args.s * 2.0])
		ze += args.z

		xm = np.mean(xe)
		zm = np.mean(ze)

		print "{0:16}{1}".format("xe", xe)
		print "{0:16}{1}".format("ze", ze)
		print "{0:16}{1}".format("xm", xm)
		print "{0:16}{1}".format("zm", zm)
	
		X,Z,F = fun_grid(p2, fun3xy, xe, ze, 20, xm, zm)
	
		Y = np.zeros(np.shape(X)) + args.y

		if args.p:
			con = pl.contourf(X,Z,F)
			pl.colorbar(con)
			pl.show()
		
		prof = fluent.profile.Profile(
				args.prof,
				'solar',
				['x','y','z','flux'],
				np.array([X,Y,Z,F]))

		print "write profile with {0} points".format(np.size(X))

		prof.write()





	
