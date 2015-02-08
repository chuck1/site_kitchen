#!/usr/bin/env python

import argparse
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument('-f', help="file")
parser.add_argument('-e', help="extensions", nargs='+')
parser.add_argument('-r', help="dry run", action="store_true")
parser.add_argument('pattern')
parser.add_argument('repl')
args = parser.parse_args()


def replace(filename):
    
    with open(filename, 'r') as f:
        rtext = f.read()


    #print rtext
    
    wtext = re.sub(args.pattern, args.repl, rtext)

    #print rtext

    if not (wtext == rtext):
        print filename
        if not args.r:
            with open(filename, 'w') as f:
                f.write(wtext)



def replace_files(exts):

    #print 'exts =', exts

    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            root, ext = os.path.splitext(filename)
            if ext in exts:
                replace(os.path.join(dirpath,filename))


if args.f:
    replace(args.f)
elif args.e:
    replace_files(args.e)
else:
    replace_files([".hpp",".cpp"])


