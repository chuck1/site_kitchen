#!/usr/bin/env python

import os
import argparse
import re
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
parser.add_argument('--prefix', help='prefix')
parser.add_argument('-n', help='dry run', action='store_true')
parser.add_argument('-v', help='verbose', action='store_true')
args = parser.parse_args()

def replace(filename, src, dst):
	
	print filename
	

	with open(filename, 'r') as f:

		wlines = []		
		rlines = f.readlines()
		
		i = 1
		
		for rline in rlines:
		
			m = re.search(src, rline)
			
			if m:
				#head += tail[:m.start(0)]
				#head += dst
				#tail = tail[m.end(0):]
				
				wline = rline[:m.start(0)] + dst + rline[m.end(0)]
				
				if args.v:
					print "{0} : {1} > {2}".format(i, repr(rline), repr(wline))
			else:
				wline = rline			
			
			wlines.append(wline)

	if not args.n:
		with open(filename, 'w') as f:
			f.writelines(wlines)


def list_header_files():
	for dirpath, dirnames, filenames in os.walk('.'):
		for filename in filenames:
			
			root, ext = os.path.splitext(filename)
	
			if ext in ['.hpp', '.hh', '.h']:
				yield os.path.join(dirpath, filename)


def move_file(src, dst):

	for filename in list_header_files():
		if args.prefix:
			replace(
				filename,
				os.path.relpath(src, args.prefix),
				os.path.relpath(dst, args.prefix))
		else:
			replace(filename, src, dst)
	
	if args.v:
		print "{0} > {1}".format(src, dst)
	
	if not args.n:
		shutil.move(src, dst)

def move_dir(src, dst):
	pass	


	


print list(list_header_files())



if os.path.isfile(args.src):
	move_file(args.src, args.dst)


if os.path.isdir(args.src):
	move_dir(args.src, args.dst)







