import math
import scipy as sci
import sys
import re
import matplotlib.pyplot as plt

#print sys.argv

#print len(sys.argv)

if len(sys.argv) < 2:
	print "usage: python read.py <filename>"
	sys.exit()

#print sys.argv[1]


sz = sci.array((0,0))

x = sci.zeros(sz,'float');
y = sci.zeros(sz,'str');

#print x


#s = 'x-coor, y-coor, vel'

f = open(sys.argv[1],'r')




i = 0
for line in f:
	split = re.split('\s*,\s*',line)
	
	sz[0] += 1
	
	sz[1] = max( sz[1], len(split) )
	#print "sz:",sz	

	x = sci.resize( x, sz )
	y = sci.resize( y, sz )
	
	for a in range( sci.size( y, 1 ) ):
		y[i,a] = ''
	
	j = 0
	for s in split:
		try:
			#print x 
			#print "i:", i
			#print "j:", j
			x[i,j] = float(s)
		except ValueError:
			y[i,j] = s
		j+=1
	i+=1


#print x
#print y


X = x[1:,1]
Y = x[1:,2]
u = x[1:,4]

print X
print Y

r = x[1:,0]

for a in range( len(X) ):
	r[a] = math.sqrt( X[a]*X[a] + Y[a]*Y[a] )


#print r


plt.plot(X,Y,'o')
plt.axis([-0.00025, 0, -0.00025, 0.00025])
plt.show()



plt.plot(r,u,'o')
#plt.axis([-0.00025, 0, -0.00025, 0.00025])
plt.show()


