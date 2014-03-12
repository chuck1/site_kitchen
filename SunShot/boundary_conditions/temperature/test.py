import numpy as np
from pylab import plot, show

n = 1

T = [10, 20, 30, 10]

A = np.zeros((n * 3,n * 3))
B = np.zeros((n * 3))

dx = 1

xe = lambda i: dx * i
xw = lambda i: dx * (i - 1)

func = lambda x,a,b,c: a*x**2 + b*x + c

for i in range(n):
	W = n-1 if i == 0 else i-1
	
	# mean
	A[i*3,i*3]   = (xe(i)**3 - xw(i)**3) / 3.0
	A[i*3,i*3+1] = (xe(i)**2 - xw(i)**2) / 2.0
	A[i*3,i*3+2] = xe(i) - xw(i)
	
	B[i*3] = T[i]

	# temperature

	A[i*3+1,i*3+0] = xw(i)**2
	A[i*3+1,i*3+1] = xw(i)
	A[i*3+1,i*3+2] = 1
	
	A[i*3+1,W*3]   = -xe(W)**2
	A[i*3+1,W*3+1] = -xe(W)
	A[i*3+1,W*3+2] = -1


	# first derivative
	A[i*3+2,i*3]   = 2 * xw(i)
	A[i*3+2,i*3+1] = 1
	
	
	A[i*3+2,W*3]   = -2 * xe(W)
	A[i*3+2,W*3+1] = -1
	
	# second derivative
	#A[i*3+2,i*3]   = 2
	
	#A[i*3+2,W*3]   = -2

print A

C = np.linalg.solve(A,B)

print C

for i in range(n):
	x = np.linspace(xw(i),xe(i))
	plot(x, func(x, C[i*3+0], C[i*3+1], C[i*3+2]))

show()





