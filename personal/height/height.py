#!/usr/bin/env python

import math
from matplotlib import cm as cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def fun1(x,r):
	return r * math.cos(x)
	
def fun2(x,r):
	return r * math.sin(x)

def cylinder(x,y,r):
        nx = x.size
        ny = y.size

	X = np.zeros((nx,ny))
	Y = np.zeros((nx,ny))
	Z = np.zeros((nx,ny))

	uX = np.zeros((nx,ny))
	uY = np.zeros((nx,ny))
	uZ = np.zeros((nx,ny))
	
	
	for i in range(nx):
		for j in range(ny):
			X[i,j] = fun1(x[i],r)
			Y[i,j] = fun2(x[i],r)
			Z[i,j] = y[j]
			
			uX[i,j] = -fun1(x[i],r) / r
			uY[i,j] = -fun2(x[i],r) / r
			uZ[i,j] = 0

			
	return X,Y,Z,uX,uY,uZ


def filt(z,w):
	Z = np.array(z)
	
	a = (2*w + 1)**2
	
        nx = np.shape(z)[0]
        ny = np.shape(z)[1]

	for i in range(nx):
		for j in range(ny):
			s = 0
			for i2 in range(-w, w + 1):
				for j2 in range(-w, w + 1):
                                        i2 += i
                                        j2 += j
                                        r = math.sqrt(i**2 + j**2)
                                        print r
					s += z[i2 if i2 < nx else i2 - nx,j2 if j2 < ny else j2 - ny]
			Z[i,j] = s/a
	return Z

def filtw(z,w):
	Z = np.array(z)
	
        nx = np.shape(z)[0]
        ny = np.shape(z)[1]

        a = range(-w,w+1)
        b = range(-w,w+1)

        A,B = np.meshgrid(a,b)

        R = np.sqrt(np.square(A) + np.square(B))
        N = np.exp(-0.1 * R)
        Nsum = np.sum(N)

        """
        print A
        print B
        print R
        print N

        plt.contourf(R)
        plt.show()
        c = plt.contourf(N)
        plt.colorbar(c)
        plt.show()
        """

	for i in range(nx):
		for j in range(ny):

                        C = A+i + (B+j) * ny

                        zsub = np.take(z, C, mode='wrap')

			Z[i,j] = np.sum(zsub * N) / Nsum
	return Z

def crater(X,Y,Z,ox,oy,r,d):

        nx = np.shape(X)[0]

	for i in range(nx):
		for j in range(np.shape(X)[1]):
			R = math.sqrt((X[0,i]-ox)**2 + (Y[j,0]-oy)**2)
			if R < r:
				Z[i][j] = d

	return Z

def perturb(X,Y,Z,uX,uY,uZ,pZ,nx,ny):

	s = 5

	for i in range(nx):
		for j in range(ny):
			X[i,j] += uX[i,j] * pZ[i,j] * s
			Y[i,j] += uY[i,j] * pZ[i,j] * s
			Z[i,j] += uZ[i,j] * pZ[i,j] * s
			
	return Z

def below(Z,z):
    Z[Z < z] = z
    return Z

def norm(Z):
    Z = Z - np.min(Z)
    Z = Z / np.max(Z)
    return Z
