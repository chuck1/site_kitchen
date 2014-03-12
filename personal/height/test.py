import math
from matplotlib import cm as cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def fun1(x,r):
	return r * math.cos(x)
	
def fun2(x,r):
	return r * math.sin(x)

def para1(x,y,nx,ny,r):
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

def filt(z,nx,ny,w):
	Z = np.array(z)
	
	a = (2*w + 1)**2
	
	for i in range(nx):
		for j in range(ny):
			s = 0
			for i2 in range(i-w,i+w+1):
				for j2 in range(j-w,j+w+1):
					s += z[i2 if i2 < nx else i2 - nx,j2 if j2 < ny else j2 - ny]
			Z[i,j] = s/a
	return Z
	
def crater(x,y,z,nx,ny,X,Y,r,d):
	
	for i in range(nx):
		for j in range(ny):
			R = math.sqrt((x[i]-X)**2 + (y[j]-Y)**2)
			if R < r:
				z[i][j] = d

	return z

def perturb(X,Y,Z,uX,uY,uZ,pZ,nx,ny):

	s = 5

	for i in range(nx):
		for j in range(ny):
			X[i,j] += uX[i,j] * pZ[i,j] * s
			Y[i,j] += uY[i,j] * pZ[i,j] * s
			Z[i,j] += uZ[i,j] * pZ[i,j] * s
			
	return Z
	
nx = 100
ny = 100

x = np.linspace(0,2*math.pi,nx+1)
y = np.linspace(0,10,ny+1)


pZ = np.random.rand(nx+1,ny+1)



pZ = filt(pZ,nx+1,ny+1,5)

#pZ = crater(x,y,Z,nx+1,ny+1,5,5,1,0.4)

pZ = filt(pZ,nx+1,ny+1,5)

X, Y, Z, uX, uY, uZ = para1(x,y,nx+1,ny+1,5)

Z = perturb(X,Y,Z,uX,uY,uZ,pZ,nx+1,ny+1)

fig = plt.figure()
ax = Axes3D(fig)

#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='RdBu', linewidth=0, antialiased=False)
ax.plot_surface(X, Y, Z,  rstride=1, cstride=1, color='b')
plt.show()


