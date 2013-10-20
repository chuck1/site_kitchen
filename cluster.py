from matplotlib import pyplot as plt
import sys
import math
import numpy as np

class clust1D:
	def __init__( self, arg ):
		self.arg = np.array([arg])
	def front( self ):
		return self.arg[0]
	def back( self ):
		return self.arg[ np.size( self.arg, 0 ) - 1 ]
	def append( self, clu ):
		self.arg = np.append( self.arg, clu.arg )
	def prnt( self ):
		print self.arg

class clusters1D:
	def __init__( self, data, dist_crit ):
		self.data = data
		self.data_len = np.size( data, 0 )
		self.dist_crit = dist_crit
		
		self.arg = np.argsort( self.data )
		
		self.clusters = []
				
		for a in range( self.data_len ):
			self.clusters.append( clust1D( self.arg[a] ) )
		
		self.alive = np.zeros(self.data_len) + 1
		
		while np.sum( self.alive ) > 1:
			print "loop"
			
			
			for a in range(len(self.clusters)):
				kill = 1
				if a < ( len(self.clusters) - 1 ):
					if ( self.dist( a, a+1 ) < self.dist_crit ):
						kill = 0
				if kill:
					self.alive[a] = 0
				
			clust_arg = np.argwhere( self.alive )
			
			print clust_arg
			
			d = np.zeros(len(clust_arg)-1)
			
			# find closest living pair
			for a in range( 0, len(clust_arg) - 1 ):
				d[a] = self.dist( clust_arg[a], clust_arg[a+1] )	
			print d
			
			a = np.argmin(d)
			b = a + 1
			
			print "a",a,"b",b
			
			# combine closest pair
			
			self.clusters[clust_arg[a]].append( self.clusters[clust_arg[b]] )
			
			self.clusters.pop(clust_arg[b])
			self.alive = np.delete( self.alive, clust_arg[b] )
	
	def dist( self, a, b ):
		if a < b:
			return math.fabs( self.data[self.clusters[a].back()] - self.data[self.clusters[b].front() ] )
		elif a > b:
			return self.dist( b, a )
		elif a == b:
			raise Exception("a==b")

	def range( self, a ):
		return math.fabs( self.data[ self.clusters[a].front() ] - self.data[ self.clusters[a].back() ] )
		

	def plot( self ):
		for a in range( len( self.clusters ) ):
			clu = self.clusters[a]
			arg = clu.arg
			plt.plot( [a]*np.size(arg), self.data[arg],'o')
		plt.show()

def test_cluster1D():
	data = np.random.rand(10)
	print data
	clu = clusters1D( data )
	clu.plot()
	for c in c.clusters:
		c.prnt()



