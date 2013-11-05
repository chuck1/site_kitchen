import re
import sys
import math
import numpy as np

search_term = sys.argv[1]
f = sys.argv[2]

pattern = re.compile(".*\s([\w-]+)\s+([\w\.]+)\s.*");

for line in open(f, 'r'):
	if re.search(search_term, line):
		if line == None:
			print 'no matches found'
		else:
			print line
			m = pattern.match(line)
			if m:
				print "match:"
				print m.groups()
				print m.group(2)
			else:
				print 'no match'

h1 = 
h2 = 
h3 = 
phi1 = 143000
phi2 = 145000
phi3 = 143000
e21 = phi2 - phi1
e32 = phi3 - phi2
r21 = 1.3
r32 = 1.3
p = 1


while 1:
	pold = p
	a = math.log( math.fabs(e32/e21) )
	e = math.copysign(1,e32/e21)
	c = math.pow(r21,p) - e
	d = math.pow(r32,p) - e
	b = math.log(c/d)
	
	p = 1 / math.log(r21) * math.fabs( a + b )
	print "p:   ",p
	print "pold:",pold
	
	arr = np.array([p,pold])
	print arr
	print np.max(arr)
	
	if ( math.fabs( (p - pold)/pold ) < 0.0001 ):
		break
