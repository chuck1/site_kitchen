#!/usr/bin/env python

import itertools
import sys
import math
#import time
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from lxml import etree

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import cluster
import data_analysis as DA
import CSV
import XML
import interpolation2 as i2
#import vector


def my_formatter_func(x, p):
	return "{0:0.1e}".format(x)
	
def plot(ax, x, y):
	ax.plot(x,y,'-o')
	
	ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(my_formatter_func))
	ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(my_formatter_func))


def plot_data( data ):
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


