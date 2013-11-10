import os
import math
import re
import sys
from lxml import etree
import numpy as np

modules_dir = os.environ["HOME"] + '/Programming/Python/Modules/'
media_dir = modules_dir + 'Sci/media/'

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
	def __init__( self, node ):
		split = re.split( "\s*", node.text )
		
		self.a = np.array([])
		
		print 'poly tag=%r' % node.tag
		print 'poly text=%r' % node.text	
		print 'split {0}'.format( split )
		
		# process coefficients
		for s in split: #len(split)-1]:
			if s:
				print "s=%r" % s
				self.a = np.append( self.a, float(s) )

	def eval( self, X ):
		if isinstance( X, float ):
			Y = np.array( [x]*len(a) )
			
			z = np.sum( a * np.power( Y, range(len(a)) ) )

			return z
		elif isinstance( X, np.ndarray ):
			Z = np.array([])
			for x in X:
				Y = np.array( [x]*len( self.a ) )

				z = np.sum( self.a * np.power( Y, range( len( self.a ) ) ) )

				Z = np.append(Z,z)
			return Z
	def integrate( self, X ):
		Y = self.eval( X )
		Z = integ( X, Y )
		return Z

		
class Property:
	def __init__( self, node ):
		self.poly = []
		
		print 'prop tag=%r' % node.tag
		
		for child in list(node):
			self.poly.append( Poly( child ) )
		
		
class Fluid:
	def __init__( self, filename ):
		self.dict = {}
		
		print "parsing '{0}'".format(media_dir + filename)
		
		tree = etree.parse( media_dir + filename )
		root = tree.getroot()
	
		print 'root tag=%r' % root.tag
		
		# process children
		for child in list(root):
			name = child.get( 'name' )
			print 'name=%r' % name
			
			if name:
				self.dict[name] = Property( child )
		
		
	def get( self, prop_name, T ):
		if prop_name in self.dict:
			prop = self.dict[prop_name]
		else:
			raise Exception("property not found")
		
		
		poly = prop.poly[0]
		
		return poly.eval( T )
		
	def enthalpy_change( self, T0, T1 ):
				
		X = frange( T0, T1, 1 )
		
		return self.dict['cp'].poly[0].integrate( X );
		
		
def integ(X,Y):
	l = len(X)
	return np.sum( ( Y[:l-1] + Y[1:] ) * ( X[1:] - X[:l-1] ) / 2 )



def np_array(X):
	if not isinstance(X,np.ndarray):
		if isinstance(X,list):
			X = np.array(X)
		else:
			X = np.array([X])
	return X


def frange(start,stop,step):
	r = start
	x = np.array(())
	while r <= stop:
		x = np.append(x,r)
		r += step
	return x

