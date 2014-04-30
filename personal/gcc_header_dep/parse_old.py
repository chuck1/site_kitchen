import re
import os
import glob

cfiles = glob.glob("*.c")
#['foo.c']

files = cfiles

dep = []

for cfile,c in zip(cfiles,range(len(cfiles))):
	
	i = [c]
	
	fileroot = cfile[:-2]
	print fileroot
	
	os.system('gcc -E ' + cfile + ' > ' + fileroot + '.pp')
	
	with open(fileroot + '.pp','r') as f:
		lines = f.readlines()
		#print lines
	
	for line in lines:
		print line
		
		m = re.search('# \d+ "([\w\/]+\.(c|h|hpp))" (\d)',line)
		if m:
			flag = int(m.group(3))
			print "match \"{0}\" {1} {2}".format(m.group(0),m.group(1),flag)
			
			
			
			# decend
			if flag==1:
				try:
					h = files.index(m.group(1))
					print "header file found",h
				except:
					files.append(m.group(1))
					h = len(files)-1
					pass
				dep.append([i[-1],h])
				i.append(h)
			elif flag==2: #ascend
				i.pop()

print cfiles
print files
print dep

filesclean = []
for file in files:
	file = re.sub('\.','',file)
	file = re.sub('\/','',file)
	filesclean.append(file)

with open('header_dep.dot','w') as f:
	f.write('digraph {\n')

	for file,fileclean in zip(files,filesclean):
		f.write("\t{0} [label=\"{1}\"]\n".format(
			fileclean,
			file))

	for d in dep:
		f.write("\t{0} -> {1}\n".format(
			filesclean[d[0]],
			filesclean[d[1]]))
	f.write('}\n')

os.system('cat header_dep.dot')



