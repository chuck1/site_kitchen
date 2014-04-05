import sys
import math
from solver import *



ind1 = [0,1,2]

ind2 = [2,3,4,5]

try:
	r1,r2 = align(ind1,ind2)
except NoIntersectError:
	print 'no intersect'
	sys.exit(0)
except EdgeError:
	print 'edge'
	sys.exit(0)


print r1
print r2

