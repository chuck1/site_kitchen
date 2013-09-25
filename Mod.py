import math
import re
import sys
from lxml import etree
import numpy as np


def get_child_by_attr(root,attr,value):
	for child in list(root):
		if child.get(attr) == value:
			return child
	return None

def process_element(root):
	print root.tag
	for child in list(root):
		process_element(child)

class Poly:
	a = {}

class Property:
	name = ""
	poly = Poly()

class Material:
	name = ""
	property = Property()

def get(root,material_name,property_name):
	
	material = get_child_by_attr(root,"name",material_name)
	if material == None:
		print "fluid not found"
		return None
	
	property = get_child_by_attr(material,"name",property_name)
	if property == None:
		print "property not found"
		return None
	
	if len(property) == 0:
		print "no poly elements found"
		return None
	
	poly = property[0]
	#print poly.text
	
	split = re.split("\s*",poly.text)
	#print split[1:len(split)-1]
	a = np.array(())
	for s in split[1:len(split)-1]:
		#print "s",s
		a = np.append(a,float(s))
	#print a	
	return a

def integ(X,Y):
	l = len(X)
	return np.sum( ( Y[:l-1] + Y[1:] ) * ( X[1:] - X[:l-1] ) / 2 )


def integ_poly(X,a):
	Y = poly_eval(X,a)
	Z = integ(X,Y)
	return Z

def np_array(X):
	if not isinstance(X,np.ndarray):
		if isinstance(X,list):
			X = np.array(X)
		else:
			X = np.array([X])
	return X

def poly_eval(X,a):
	X = np_array(X)
	Z = np.array(())
	for x in X:
		Y = np.zeros(len(a))
		Y.fill(x)
		z = np.sum( a * np.power( Y, range(len(a)) ) )
		Z = np.append(Z,z)
	return Z

def frange(start,stop,step):
	r = start
	x = np.array(())
	while r <= stop:
		x = np.append(x,r)
		r += step
	return x

