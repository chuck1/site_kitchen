#!/usr/bin/env python

import re

from parser import *

if __name__ == '__main__':
	with open('test.cpp','r') as f:
		lines = f.readlines()
	
	lines = preprocess(lines)

	#for l in lines:
	#    print repr(l)

	gchunk = ChunkNone(None, lines)

	process(gchunk)

	gchunk.printvar()

	#for k in gchunk.keep:
	#    print repr(k)
	#print gchunk.scope

	for l in gen_full(gchunk):
		print l

