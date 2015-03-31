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

pat = '# \d+ "([-\.\w\/]+\.(cpp|c|h|hpp))"( \d)?( \d)?( \d)?'

def make_graph(files, args, dep, ):
    depflat = [d for subl in dep for d in subl]
    filesclean = []
    filesp = []
    for file in files:
        filesp.append(prefixed(file,args))
	file = re.sub('\.','',file)
	file = re.sub('\/','',file)
	file = re.sub('-','',file)
        #print file
        filesclean.append(file)
    
    G=nx.DiGraph()

    nodes = {}

    with open('header_dep.dot','w') as f:
	f.write('digraph {\n\trankdir=RL\n')

        # create all nodes first
	for filename,fnp,fileclean,i in zip(files,filesp,filesclean,range(len(files))):

            if not args.s and issys(filename):
                continue

	    if i in depflat:
                # if prefix specified, use it to shorten names
                if args.p:
                    if not filename[0:5] == '/usr/':
                        filename = os.path.relpath(filename, args.p)
		
                f.write("\t{0} [label=\"{1}\"]\n".format(
		    fileclean,
		    filename))

                #print "create node:", filename
                n = Node(fnp)
                G.add_node(n)
                nodes[filename] = n
        
        # create all edges
	for d in dep:
                #print "create edge"
		f0 = filesp[d[0]]
		f1 = filesp[d[1]]
      
                try:
                    n0 = nodes[f0]
                    n1 = nodes[f1]
                except:
                    pass
                else:
                    #print f0
                    #print f1
                    f.write("\t{0} -> {1}\n".format(
	    		    filesclean[d[0]],
	    		    filesclean[d[1]]))

       
                    logging.debug("{0}--->{1}".format(n0, n1))

                    G.add_edge(n0,n1)

	f.write('}\n')

    return G


def issys(s):
    return s[0:5] == "/usr/"

def prefixed(fn, args):
    if args.p:
        if not fn[0:5] == '/usr/':
            fn = os.path.relpath(fn, args.p)
    return fn

def precom(filename):
    cmd = ['gcc', '-E', '-I.', filename]
    print "cmd=",cmd
	
    print "stdout=", filename + '.pre'

    with open(filename + '.pre', 'w') as f:
        subprocess.call(cmd, stdout=f)

    
    cmd = ['./pre_to_pre2.py', filename + '.pre']
    print cmd
    subprocess.call(cmd)

def get_c_files(args):
    cfiles = list(myos.glob(".*\.c$", args.d))
    ccfiles = list(myos.glob(".*\.cpp$", args.d))
    cfiles += ccfiles
    return cfiles


class Node(object):
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return self.filename

def print_degree(g, l = False, ff = None):
    c = 0
    d = g.out_degree()

    if not d:
        return 0
    
    s = sorted(d.items(), cmp = lambda x,y: cmp(x[1],y[1]))
    s = filter(lambda x: ff(x[0].filename), s)
    if not s:
        return 0
    m = min(i[1] for i in s)
    #print "min", m
    for i in s:
        if l:
            if i[1] == m:
                c += 1
                #print i[0]
                print after_include(i[0].filename)
            else:
                return c
        else:
            print i[0]
            #print i[0]
    return c

def remove_zero(g):
    d = g.out_degree()
    for i in sorted(d.items(), cmp = lambda x,y: cmp(x[1],y[1])):
        if i[1] == 0:
            g.remove_node(i[0])

def is_header(filename):
    return filename[-4:] == ".hpp"

def after_include(filename):
    #print filename
    lst = []
    h,t = os.path.split(filename)
    while t:
        if t == 'include':
            break
        else:
            lst.append(t)

        h,t = os.path.split(h)

    return os.path.join(lst)[0]

class Item(object):
    def __init__(self, name, flags):
        self.name = name
        self.flags = flags

class Pre2(object):
    def __init__(self):
        self.items = []

def pre_to_pre2(filename):
    

    with open(filename, 'r') as f:
        lines = f.readlines()
   
    lines2 = []

    p = Pre2()
    
    for line in lines:
        m = re.search(pat, line)
	if m:
            name = m.group(1)
            #print name
            
            g = list(m.groups())
	    g = g[2:]
	    flags = []
            flags = list(int(a) for a in g if a)
	    #for a in g:
	    #    if a:
	    #        flags.append(int(a))
            
            lines2.append(line)
            
            p.items.append(Item(name, flags))

    with open(filename + "2", 'w') as f:
        #f.write("".join(lines2))
        pickle.dump(p, f)






