#!/usr/bin/env python
import re
import os
import glob
import myos
import sys
import subprocess
import argparse


i = 0

dep = []

files = []

#root = '\/nfs\/stak\/students\/r\/rymalc\/usr\/include'
root = __file__

def process(fileto,flags,filetype):
	global i

	#print fileto[:4],fileto[:4]=="/usr"
	if fileto[:4]=="/usr":
		flag = 3
		#pass
	
	fileto = re.sub(root,'',fileto)
	
	
	if 1 in flags or 3 in flags: # decend
		try:
			h = files.index(fileto)
			#print "header file found",h
		except:
			files.append(fileto)
			filetype.append(flags)

			h = len(files)-1
			#print "appending \"{0}\" to files".format(m.group(1))
		
		
		if i==h: #if i[-1]==h:
			#print "skip(already in)                 \"{0}\"".format(fileto)
			pass
		else:
			if 3 in filetype[i]: #elif filetype[i[-1]]==3:
				#print "skip(currently in system header) \"{0}\"".format(fileto)
				pass
			else:	
				newdep = [i,h] #newdep = [i[-1],h]
				if not newdep in dep:
					dep.append(newdep)
		
			print "descend   from \"{0:40}\":{1:10} to \"{2:40}\":{3}".format(
						files[i],
						filetype[i],
						fileto,
						flags)
			i = h #i.append(h)
			
			#print "i=",i

	elif 2 in flags: #ascend
		
                try:
                    j = files.index(fileto)
                except:
                    files.append(fileto)
                    j = files.index(fileto)

		print "ascending from \"{0:40}\":{1:10} to \"{2:40}\":{3}".format(
				files[i],
				filetype[i],
				files[j],
				filetype[j])

		
		
		#print line

		i = j #i.pop()
		
		#print "i=",i
	else:
		print "don't care about..."
		print line[0:-2]



def precom(filename):
    cmd = ['gcc', '-E', '-I.', filename, '>', filename + '.pre']
    cmd = ['gcc', '-E', '-I.', filename]
    print "cmd=",cmd
	
    print "stdout=", filename + '.pre'

    with open(filename + '.pre', 'w') as f:
        subprocess.call(cmd, stdout=f)


def get_c_files():
    cfiles = list(myos.glob(".*\.c$", d))
    ccfiles = list(myos.glob(".*\.cpp$", d))
    cfiles += ccfiles
    return cfiles






parser = argparse.ArgumentParser()
parser.add_argument("-d", help="directory")
parser.add_argument("-p", help="path prefix for label")
parser.add_argument("-c", action='store_true', help="do the precompiling")
args = parser.parse_args()

if args.d:
    d = args.d
else:
    d = '.'


#['foo.c']

#


if args.c:
    
    c_files = get_c_files()
    
    for f in c_files:
        precom(f)
 
    pre_files = list(f + '.pre' for f in c_files)
   
else:
    pre_files = list(myos.glob(".*\.c\.pre$", d))
    pre_files += list(myos.glob(".*\.cpp\.pre$", d))


filetype = [[1]]*len(pre_files)

print "filetype",filetype
print "pre_files",pre_files

for pre_file,c in zip(pre_files,range(len(pre_files))):
	
	print "parsing file \"{0}\"".format(pre_file)
        
	i = c
	
	#fileroot = cfile[:-2]
	#print "fileroot=",fileroot
	
        
        #subprocess.call(cmd)
        #P = subprocess.Popen(cmd, stdout=PIPE)
        
	with open(pre_file, 'r') as f:
		lines = f.readlines()
		#print lines
	
	newlines = []
	for line in lines:
		if line[0]=='#':
			newlines.append(line)
			#print line[:-1]
	
	lines = newlines
	
	for line in lines:
		print "line=",repr(line)
		
		
		m = re.search('# \d+ "([\w\/]+\.(cpp|c|h|hpp))"( \d)( \d)?( \d)?',line)
		if m:
			print "groups=",len(m.groups())
			g = list(m.groups())
			g = g[2:]
			print "g",g
			flags = []
			for a in g:
			    if a:
				#print "a",a
				flags.append(int(a))
			
			print "flags=", flags
			fileto = m.group(1)
			print "line[:-1]=", repr(line[:-1])
			#print "match \"{0}\".format(m.group(0))
				
			process(fileto,flags,filetype)
		else:
                        print "no match"
			pass
			#m = re.search('# \d+ "([\w\/]+\.(c|cpp|h|hpp))"',line)
			#if m:
			#	fileto = m.group(1)
			#	if fileto==cfile:
			#		print "return to c file"
			#
			#		process(fileto,1)	


#print cfiles
print "files:", files
print "dep:",dep

filesclean = []
for file in files:
	file = re.sub('\.','',file)
	file = re.sub('\/','',file)
	file = re.sub('-','',file)
        print file
        filesclean.append(file)

depflat = [d for subl in dep for d in subl]

with open('header_dep.dot','w') as f:
	f.write('digraph {\n\trankdir=BT\n')

	for file,fileclean,i in zip(files,filesclean,range(len(files))):
	    if i in depflat:
                # if prefix specified, use it to shorten names
                if args.p:
                    if not file[0:5] == '/usr/':
                        file = os.path.relpath(file, args.p)
		
                f.write("\t{0} [label=\"{1}\"]\n".format(
		    fileclean,
		    file))

                nx graph add node

	for d in dep:
		f.write("\t{0} -> {1}\n".format(
			filesclean[d[0]],
			filesclean[d[1]]))

                
                nx graph add edge

	f.write('}\n')

#os.system('cat header_dep.dot')

cmd = ["dot", "-Tpng", "header_dep.dot", "-oheader_dep.png"]

subprocess.call(cmd)

