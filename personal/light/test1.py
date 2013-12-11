#!/usr/bin/env python

import numpy as np

# input
n = 10
u0 = 10




# solve

B = np.zeros(n)
s = np.zeros(n)
a = np.zeros(n) + 1;

A = np.zeros((n,n))
for r in range(n-1):
	A[r,r] = 1
	A[r,r+1] = -1
	B[r] = a[r] + s[r+1] - s[r]
	
	
A[n-1,0] = 1
B[n-1] = u0

print "s",s
print "a",a
print "B",B
print A

Ai = np.linalg.inv(A)

u = np.linalg.solve(A,B)

print u

