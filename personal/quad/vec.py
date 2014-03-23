import numpy as np
import math

e2 = np.array([0.,0.,1.])

def sign(x):
	return math.copysign(1.0,x)

def clamp(x,minx,maxx):
	if x > maxx:
		print 'max',maxx
		return maxx
	elif x < minx:
		print 'min',minx
		return minx
	else:
		return x

def clampz(x,v):
	return clamp(x,-v,v)

def magsq(a):
	return np.sum(np.square(a))
def mag(a):
	return math.sqrt(magsq(a))

def set_arb_comp(a,b):
	am = mag(a)
	ah = a / am

	bm = mag(b)
	bh = b / bm
	
	bm2 = am / np.dot(ah,bh)
	
	return bm2

def angle(a,b,up,ver = False):
	# rotation between a and b
	a_norm = np.linalg.norm(a)	
	b_norm = np.linalg.norm(b)
	
	if a_norm == 0 or b_norm == 0:
		return None,None,None,None
	
	d = np.dot(a,b)
	
	#d_angle = math.acos(d / a_norm / b_norm)
	
	c = np.cross(a,b)
	
	d_up = np.dot(c,up)
	
	c_norm = np.linalg.norm(c)
	
	
	
	c_angle = math.asin(c_norm / a_norm / b_norm)
	
	if d < 0:
		c_angle = math.pi - c_angle

	if d_up < 0:
		c_angle = -c_angle
	

	if ver:
		print 'd      ',d
		print 'd_up   ',d_up
		print 'c_angle',c_angle
		print 'c_norm ',c_norm
	
	
	return c, c_norm, c_angle, d_up


if __name__ == '__main__':
	a = np.array([1.,0.,0.])
	
	angle(a,np.array([ 1., 1.,0.]),e2, ver=True)
	angle(a,np.array([-1., 1.,0.]),e2, ver=True)
	angle(a,np.array([-1.,-1.,0.]),e2, ver=True)
	angle(a,np.array([ 1.,-1.,0.]),e2, ver=True)





