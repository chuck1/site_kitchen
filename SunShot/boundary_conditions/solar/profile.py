#!/usr/bin/env python

import sys, os
import numpy as np
import matplotlib.pyplot as plt

module_dir = os.environ["HOME"] + "/Documents/Programming/Python/Modules/"
sys.path.append(module_dir)

import mycsv

# a*(x*x + y*y) + b*(x + y) + c

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
	

if len(sys.argv) != 2:
	print "usage: {0} file"
	sys.exit(1)


filename = sys.argv[1]
#c = float(sys.argv[2])
#e = float(sys.argv[3])


# half width
w = 1.5e-2 + 0.000886

data = mycsv.read(filename)

x = data[:,0]
y = data[:,1]

x = x * 1e-3
y = y * 1e4

x = x - w

#print x

#i = np.argsort(x)
#x = x[i]
#y = x[i]

#print x

p1 = np.polyfit(x, y, 2)

#p2 = p1

#p2[2] += scale(4e6*w*w, w, p1)

#print integrate_poly2d(w, p1)
#print integrate_poly2d(w, p2)


f = np.poly1d(p1)

#print p2

x2 = np.sort(x)

# normal distribution
x3 = np.power(x,2)
y3 = np.log(y)

p3 = np.polyfit(x3, y3, 1)
f3 = np.poly1d(p3)

"""
plt.plot(x3,y3,'o')
plt.plot(x3,f3(x3),'s')
plt.show()
"""

print "p3 =",p3
l3 = lambda x: np.exp(f3(np.square(x)))

print p1
print "parabola vertex x =",-p1[1] / 2. / p1[0]





plt.plot(x,y,'o')
plt.plot(x2,f(x2),'-')
plt.plot(x2,l3(x2),'-')

plt.xlabel('position (m)')
plt.ylabel('heat flux (W/m2)')
plt.legend(['experimental','parabola','normal distribution'], loc='lower center')




plt.show()



















sys.exit(0)






w = 1e-3

# curvature based on measured peak and edge values
a = parab_2d_coeff_from_meas( c, e, w/2 )
b = a;

# initial ingeral
S0 = integrate( -w/2, w/2, -w/2, w/2, a, b, c )

# desired integrated value
S = 4e6 * w * w;


# adject peak to give desired integral value
#c = scale( S, (min[0]-xc), (max[0]-xc), (min[2]-zc), (max[2]-zc), a, b )

S1 = integrate( (min[0]-xc), (max[0]-xc), (min[2]-zc), (max[2]-zc), a, b, c )

plot2d(filename,a,c)



sys.exit(0)

#print "S0={0}".format(S0)
#print "S1={0}".format(S1)



x = np.arange(101) / 100.0 * w + min[0]
z = np.arange(101) / 100.0 * rng[2] + min[2]

X,Z = np.meshgrid(x,z)

s = a*X*X + b*Z*Z + c

CS = plt.contourf(X,Z,s)
CB = plt.colorbar(CS,format='%e')
CB.set_label('heat flux (W/m2)')
plt.axis('equal')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')


plt.show()





