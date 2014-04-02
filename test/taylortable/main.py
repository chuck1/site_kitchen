import numpy as np
import math


def ttrow(i, d, n):
	#print "i",i,"d",d,"n",n
	
	a = np.zeros(n)
	for j in range(n):
		if j >= d:
			den = math.factorial(j-d)
			#print den
			a[j] = i**(j-d) / den

	
	#print "a",a
	
	return a

#i = [0 0 1 2 0];
#d = [1 0 0 0 3];


# APPLIES TO UNIFORM GRID
# i is the index or location
# d is the orderof the term
# X is a coefficient of the terms not including the first
# the coefficnet of the first term is one


#i = [1, 0, 0, 1]
#d = [1, 1, 2, 2]

i = [0,  0, -1, -1]
d = [1,  0,  1,  0]

m = len(i)
n = m-1


#T = sym(zeros(m,n))
T = np.zeros((m,n))

for j in range(m):
	T[j,:] = ttrow(i[j],d[j],n)



A = np.transpose(T[1:m,0:m-1])

b = -T[0,0:m-1]
b = np.reshape(b, (1,n))
b = np.transpose(b)

ver = False
if ver:
	print "m",m,"n",n
	print "T"
	print T
	print "A"
	print A
	print "b"
	print b

X = np.dot(np.linalg.inv(A), b)

print "i",i
print "d",d
print "X"
print X

