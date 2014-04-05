from sympy import *
import numpy as np

def A(q):
	q = np.array(np.reshape(q,(4)))
	return np.array([
		[ q[0],  q[1],  q[2],  q[3]],
		[-q[1],  q[0], -q[3],  q[2]],
		[-q[2],  q[3],  q[0], -q[1]],
		[-q[3], -q[2],  q[1],  q[0]]])

def B(q):
	q = np.reshape(q,(4))
	return np.array([
		[ q[0], -q[1], -q[2], -q[3]],
		[ q[1],  q[0], -q[3],  q[2]],
		[ q[2],  q[3],  q[0], -q[1]],
		[ q[3], -q[2],  q[1],  q[0]]])

def quat(q):
	q = np.array([[q[0], q[1], q[2], q[3]]])
	q = np.reshape(q, (4,1))
	return q

def conj(q):
	q = np.array([[q[0], -q[1], -q[2], -q[3]]])
	q = np.reshape(q, (4,1))
	return q


a = quat(symbols('a0:4'))
b = quat(symbols('b0:4'))


print np.shape(A(a))
print np.shape(b)

c = np.dot(B(a), b)
d = np.dot(A(conj(b)), a)

e = np.dot(A(a), b)
f = np.dot(B(b), conj(a))



print c == d
print e == f


