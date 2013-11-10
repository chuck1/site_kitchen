#!/usr/bin/env python

print "hellO"

import re
import os
import sys
import math
import numpy as np
import lxml.etree as etree
import logging

print "hello"

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import Sci.Geo as Geo
import XML

logging.basicConfig(level=logging.DEBUG)

def extract2( f, find_str, ext_str, offset ):
	find_pat = re.compile( find_str )
	ext_pat = re.compile( ext_str )
	
	found = 0
	offset -= 1
	
	for line in open(f, 'r'):
		#print 'line=%r' % line
		if found:
			if offset == 0:
				#print "extract line=%r" % line
				return ext_pat.match(line)
			else:
				offset -= 1
		else:
			m = find_pat.match(line)
			#print 'found=0,m=',m
			if m:
				found = 1
	return None

def extract( str_search, str_pattern, str_filename ):
	#pattern = re.compile(".*\s([\w-]+)\s+(-?[\w\.]+)\s.*");
	pattern = re.compile( str_pattern )
	
	ret = ""
	
	for line in open( str_filename, 'r' ):
		if re.search( str_search, line ):
			#print 'line=%r' % line
			if line == None:
				print 'no matches found'
			else:
				m = pattern.match(line)
				if m:
					return m.group(1)
				else:
					raise Exception( "no match for %r in %r" % (str_pattern, line) )

def grid_refinement(phi,h):
	# make sure r > 1
	arg = np.argsort(h)
	phi = phi[arg]
	h = h[arg]
	
	
	e21 = phi[1] - phi[0]
	e32 = phi[2] - phi[1]
	r21 = float(h[1]) / float(h[0])
	r32 = float(h[2]) / float(h[1])
	
	p = 1
	
	print "phi={0}".format(phi)
	print "n  =",n
	print "h  =",h

	print "r21=",r21
	print "r32=",r32
	print "e21=",e21
	print "e32=",e32
	
	a = math.log( math.fabs(e32/e21) )
	e = math.copysign(1,e32/e21)
		
	while 1:
		pold = p
		
		
		
		c = math.pow(r21,p) - e
		d = math.pow(r32,p) - e
		b = math.log(c/d)
		
		p = 1 / math.log(r21) * math.fabs( a + b )
		#print "p:   ",p
		#print "pold:",pold
		
		arr = np.array([p,pold])
		arr = np.absolute(arr)
		arr_max = np.max(arr)
		
		if arr_max == 0:
			break
		
		if ( math.fabs( (p - pold)/pold ) < 0.0001 ):
			break
	
	print "p:  ",p
	
	gci = math.fabs( ( phi[0] - phi[1] )/( 1 - math.pow(r21,p) ) )
	
	print "gci:",gci
	
	err = np.abs(gci/phi)
	print "percent err:",err*100
	
	err_tar = 0.03
	gci_tar = math.fabs(err_tar * phi[0])
	h_tar = h[0] * math.pow(gci_tar/gci,1.0/p)
	
	
	
	n_tar = v / math.pow(h_tar,3)
	
	
	print
	print "err_tar:",err_tar
	print "gci_tar:",gci_tar
	print "h_tar:",h_tar
	print "n_tar:",n_tar/1.0e6," million"

#############################################################################################################

# this program calculates the GCI for a grid refinement study
# <folder> should contain folders named case_X where X is 0, 1, and 2

if len( sys.argv ) != 3:
	print "usage: %r <folder> <value>"%sys.argv[0]
	sys.exit(0)

folder = sys.argv[1]
value_string = sys.argv[2]

#----------------------------------------------------------------


xmlfilename = folder + "exp.xml"

tree = etree.parse( xmlfilename )
root = tree.getroot()

v = Geo.volume( root.find('geo') )

print "v={0:e}".format(v)



#str_pattern_metric = "\w+\s+(-?[\w\.\-\+]+)\s.*"

#report_file_str = sys.argv[2]
#str_search_metric = sys.argv[3]
#v = float( sys.argv[4] )

phi = np.zeros(3)
n = np.zeros(3)


for a in range(0,3):
	# extract metrix from file
	#filename_metric = folder +"case_" + str(3-a) + "/"+report_file_str

	#phi[a] = float( extract( str_search_metric, str_pattern_metric ,filename_metric ) )
	# get instead from xml file
	val_str = ['exp','out','case{{id={0:d}}}'.format(a),'val{{name={0:s}}}'.format(value_string)]
	val = XML.find(root, val_str)
	phi[a] = float(val.text)
	
	
	
	# extract number of grid cells from file
	res = extract2( folder + "case_{0:d}".format(a) + "/job.log.out", 'Mesh Size', '^\s*([0-9]+)\s+([0-9]+)\s+.*', 3 )
	n[a] = int( res.group(2) )
	

#v = 1e-2 * ( 150e-6 + 465.5e-6 ) * ( 200e-6 + 180e-6 + 2e-3 )
#v = 1.767145868E-09

print "volume = %10e" % v

h = np.power( v/n, 1.0/3.0 )


grid_refinement(phi,h)


