import markdown
import argparse
import re
import os
import sys
import shutil

def change_ext(path):
	
	root,ext = os.path.splitext(path)

	if ext == '.html':
		ext = '.md'
	elif ext == '.md':
		ext = '.html'
	

	return root + ext

def fix_links_md(md_file, src, dst):
	count = 0

	#print "fixing:",repr(md_file)

	with open(md_file, 'r') as f:
		tail = f.read()
	
	# links are relative, so we need the dir of this file
	md_dir = os.path.dirname(md_file)
	
	src_rel = os.path.relpath(src, md_dir)

	# store processed string
	head = ''
	
	src2 = change_ext(src_rel)
	
	#print "src2 =",repr(src2)
	
	src2_esc = src2.replace('/','\/')

	#print "src2_esc =",repr(src2_esc)

	# prepare the destination
	dst2 = change_ext(dst)
	dst2_rel = os.path.relpath(dst2, md_dir)
	
	str = '\[.*?\]\((' + src2_esc + ').*?\)'
	
	match = re.search(str, tail)
	while match:
		count += 1
		# search for links

		print "match in",repr(md_file)
		#print match.group(1)
		#print match.start(1)
		#print match.end(1)
		
		head += tail[:match.start(1)]
		
		head += dst2_rel
		
	

		tail = tail[match.end(1):]
		
		match = re.search(str, tail)

	if count > 0:
	
		head += tail
	
		#print head

		with open(md_file, 'w') as f:
			f.write(head)

#####################

parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()

if not os.path.isfile(args.src):
	print "file does not exist"
	sys.exit(1)

for root, dirs, files in os.walk('.'):
	for file in files:
		roo,ext = os.path.splitext(file)
		if ext == '.md':
			path = os.path.join(root,file)
			path = os.path.normpath(path)
			#print path
			fix_links_md(path, args.src, args.dst)


dst_dir = os.path.dirname(args.dst)

if not os.path.exists(dst_dir):
	 os.makedirs(dst_dir)

shutil.move(args.src, args.dst)

print "move {0} to {1}".format(repr(args.src),repr(args.dst))

