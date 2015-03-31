#!/usr/bin/env python

import pickle
import re
import os
import glob
import myos
import sys
import subprocess
import argparse
import networkx as nx
import logging

from func import *

i = 0



dep = []
files = []
filetype = []

#root = '\/nfs\/stak\/students\/r\/rymalc\/usr\/include'
root = __file__


def index_of(fn, flags = []):
    try:
	i0 = files.index(fn)
	#print "header file found",h
    except:
	files.append(fn)
	filetype.append(flags)
        
	i0 = len(files)-1
    return i0

def process(fileto,flags,filetype):
    global i
    logging.debug("process: in file {0}".format(files[i]))
    logging.debug("process: fileto  {0}".format(fileto))
    logging.debug("process: flags   {0}".format(flags))
    #print fileto[:4],fileto[:4]=="/usr"
    if fileto[:4]=="/usr":
	flag = 3
	#pass
    
    fileto = re.sub(root,'',fileto)
    
    if 1 in flags or 3 in flags:
        h = index_of(fileto, flags)

	if i==h: #if i[-1]==h:
	    logging.debug("skip(already in)                 \"{0}\"".format(fileto))
	else:
	    if 3 in filetype[i]: #elif filetype[i[-1]]==3:
		    #print "skip(currently in system header) \"{0}\"".format(fileto)
                    logging.debug("issys {0}".format(files[i]))
            elif issys(files[i]):
                    logging.debug("issys {0}".format(files[i]))
	    else:	
                    logging.debug("create dep")
	            newdep = [i,h] #newdep = [i[-1],h]
		    if not newdep in dep:
				dep.append(newdep)
	
    	    logging.debug("descend   from \"{0:40}\":{1:10} to \"{2:40}\":{3}".format(
		  	    files[i],
			    filetype[i],
			    fileto,
			    flags))

	    i = h #i.append(h)

    elif 2 in flags or fileto[-4:] == '.cpp': #ascend
	j = index_of(fileto)

	logging.debug("ascending from \"{0:40}\":{1:10} to \"{2:40}\":{3}".format(
			files[i],
			filetype[i],
			files[j],
			filetype[j]))

	i = j
		

parser = argparse.ArgumentParser()
parser.add_argument("-d", help="directory", default=".")
parser.add_argument("-p", help="path prefix for label")
parser.add_argument("-c", action='store_true', help="do the precompiling")
parser.add_argument("-r", action='store_true', help="render dot")
parser.add_argument("-v", action='store_true', help="verbose")
parser.add_argument("-s", action='store_true', help="display system headers")
args = parser.parse_args()

if args.v:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


if args.c:
    c_files = get_c_files(args)
    
    for f in c_files:
        precom(f)
 
    pre_files = list(f + '.pre2' for f in c_files)
   
else:
    pre_files = list(myos.glob(".*\.c\.pre2$", args.d))
    pre_files += list(myos.glob(".*\.cpp\.pre2$", args.d))


logging.debug("\n".join(pre_files))


logging.info("number of precompiler files: {}".format(len(pre_files)))

def pre2_to_pre3(pre_file):

        filename = pre_file[:-5]
        
        i = index_of(filename)
        
        with open(pre_file, 'r') as f:
	    #lines = f.readlines()
            p = pickle.load(f)
	
        pat = '# \d+ "([-\w\/]+\.(cpp|c|h|hpp))"( \d)?( \d)?( \d)?'
        
	#for line in lines:
	for item in p.items:
                fileto = item.name
                flags = item.flags
			
                if not issys(fileto):
                    pass
                
		process(fileto,flags,filetype)

i0 = 0

for pre_file in pre_files:
    if not args.v:
       sys.stdout.write("\r{:8}".format(i0))
       sys.stdout.flush()
       i0 += 1

    pre2_to_pre3(pre_file)

print

G = make_graph(files, args, dep, )

if args.r:
    cmd = ["dot", "-Tpng", "header_dep.dot", "-oheader_dep.png"]
    subprocess.call(cmd)

i = 0
while True:
    c = print_degree(G, True, is_header)
    if c == 0:
        break
    remove_zero(G)
    i += 1


