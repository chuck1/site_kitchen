#!/usr/bin/env python

import sys
import os
import numpy as np
import csv
import matplotlib.pyplot as plt

module_dir = os.environ["HOME"] + "/Programming/Python/Modules/"
sys.path.append(module_dir)

import CSV

if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print "Usage: {0} filename [delimiter-pattern]".format(sys.argv[0])
		sys.exit(0)

	filename = sys.argv[1]
	
	if len(sys.argv) > 2:
		delim = (sys.argv[2]).decode('string_escape')
	else:
		delim = ','

	print "delim='{0}'".format(delim)

	data = CSV.read(filename, delim)

	print data
	print np.shape(data)
	
	for i in range(0,np.size(data,1)):
		plt.semilogy(data[:,i])
	
	plt.show()
