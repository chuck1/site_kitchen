import itertools
import sys
import math
#import time
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import cluster
import data_analysis as DA
import CSV
import XML
import interpolation2 as i2
#import vector

def print_data( data ):
	plt.figure()
	plt.plot(data[:,1],data[:,2],'o')
	plt.show()

def print_data2( data, arg ):
	plt.figure()
	plt.plot(data[:,1],data[:,2],'o')
	
	plt.plot(data[arg,1],data[arg,2],'s')
	
	#plt.figure()
	#plt.plot( r, data[arg,j], 'o' )
	
	plt.show()

# ------------------------------------------

# filename = 'export.dat'
# z = 22e-3

usage = "usage: python {0:s} <filename> <x> <y> <z>".format(sys.argv[0])

if len(sys.argv) < 5:
	print usage
	sys.exit(1)

filename = sys.argv[1]
x = float( sys.argv[2] )
y = float( sys.argv[3] )
z = float( sys.argv[4] )

print "file={0:s}".format(filename)

# ------------------------------------

dir = os.getcwd()

case_id = int(re.search("case\_(\d+)", dir).group(1))

# ----------------------------------------
z_ind = 3

tol = 1e-7

tol_init = 1e-6

# get data

sys.stdout.write("converting csv file to numpy array...")
sys.stdout.flush()

data = CSV.read(filename)

sys.stdout.write(" returned {0} array\n".format(np.shape(data)))

# take z-slice

sys.stdout.write("taking z-slice...")
sys.stdout.flush()

data = data[ ( data[:,z_ind] < ( z+tol_init ) ) & ( data[:,z_ind] > ( z-tol_init ) ), : ]

sys.stdout.write(" returned {0} array\n".format(np.shape(data)))

 

#clus = cluster.clusters1D( data[:,z_ind], 1e-6 )
#clu = clus.closest_to( z )
#data = data[ clu.arg, : ]
#print "shape(data)", np.shape(data)

#print_data( data )




# find nearest points along a line ---------------------------------------------------

# interp stencil
m = np.array([4])
# interp variable column index
i = np.array([1,2])
# temperature column index
j = 4
# direction
dir = np.array([0,1])

arg,r = DA.nearest_in_direction( np.array([x,y]), data[:,i], m[0], dir )

#print np.shape(r)
#print r

print_data2(data,arg)


# --------------------------------------------

s = i2.spline( m, r, data[arg,j] )
grad = s.eval_grad_single( np.array([0]) )
grad = grad[0]
#print grad

print "output_gradient %e" % grad



#cond = 16
#flux = -cond * grad
#print "flux %e" % flux

# append xml for experiment ----------------------------------

filename = "../exp.xml"
tree = etree.parse(filename)
root = tree.getroot()

str = [
	"exp",
	"out",
	"case{{id={0:d}}}".format(case_id),
	"val{{name=grad1}}({0:f})".format(grad)]

XML.insert(root, str)

tree.write(filename)






