#!/usr/bin/env python

import re

from parser import *
from Chunk import *

import argparse

def do_file(filename):

    colors.draw(filename, fg_green=True)

    with open(filename,'r') as f:
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

    #for l in gen_full(gchunk):
    #print l


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    if args.files:
        for filename in args.files:
            do_file(filename)
        

