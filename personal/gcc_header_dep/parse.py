import re
import os
import glob
import sys
import fnmatch

cfiles = []
for root, dirnames, filenames in os.walk('.'):
	for filename in fnmatch.filter(filenames, '*.cc'):
		cfiles.append(os.path.join(root, filename))


#['foo.c']

files = cfiles
filetype = [[1]]*len(cfiles)
i = 0

dep = []

def process(fileto,flags):
	global i

	#print fileto[:4],fileto[:4]=="/usr"
	if fileto[:4]=="/usr":
		flag = 3
		#pass
	
	fileto = re.sub('\/nfs\/stak\/students\/r\/rymalc\/usr\/include','',fileto)
	
	
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



for cfile,c in zip(cfiles,range(len(cfiles))):
	
	print "parsing file \"{0}\"".format(cfile)

	i = c
	
	fileroot = cfile[:-2]
	print fileroot
	
	os.system('gcc -E -I. ' + cfile + ' > ' + cfile + '.pre')
	
	with open(cfile + '.pre','r') as f:
		lines = f.readlines()
		#print lines
	
	newlines = []
	for line in lines:
		if line[0]=='#':
			newlines.append(line)
			print line[:-1]
	
	lines = newlines
	
	for line in lines:
		#print line
		
		
		m = re.search('# \d+ "([\w\/]+\.(cpp|c|h|hpp))"( \d)( \d)?( \d)?',line)
		if m:
			#print "groups=",len(m.groups())
			g = list(m.groups())
			g = g[2:]
			#print "g",g
			flags = []
			for a in g:
				if a:
					#print "a",a
					flags.append(int(a))
			
			#print flags
			fileto = m.group(1)
			print line[:-1]
			#print "match \"{0}\".format(m.group(0))
				
			process(fileto,flags)
		else:
			pass
			#m = re.search('# \d+ "([\w\/]+\.(c|cpp|h|hpp))"',line)
			#if m:
			#	fileto = m.group(1)
			#	if fileto==cfile:
			#		print "return to c file"
			#
			#		process(fileto,1)	

print cfiles
print files
print dep

filesclean = []
for file in files:
	file = re.sub('\.','',file)
	file = re.sub('\/','',file)
	filesclean.append(file)

depflat = [d for subl in dep for d in subl]


with open('header_dep.dot','w') as f:
	f.write('digraph {\n')

	for file,fileclean,i in zip(files,filesclean,range(len(files))):
		if i in depflat:
			f.write("\t{0} [label=\"{1}\"]\n".format(
				fileclean,
				file))

	for d in dep:
		f.write("\t{0} -> {1}\n".format(
			filesclean[d[0]],
			filesclean[d[1]]))
	f.write('}\n')

#os.system('cat header_dep.dot')



