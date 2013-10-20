#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt

class pid:
	#def __init__(self):	
	p = 1
	i = 0
	d = -1
	integral = 0
	derivative = 0
	target = 0
	x = 0
	v = 0
	target = 1
	
	def step(self,dt):
				
		e = self.target - self.x
		
		self.v += ( self.p * e + self.i * self.integral + self.d * self.v ) * dt
		self.x += self.v * dt


n = int(sys.argv[1])

dt = 0.01

t=[0]*n
x=[0]*n

c = pid()

for a in range(1,n):
	t[a] = t[a-1] + dt
	print "t[%2i]=%4.2f" % (a,t[a])
	c.step(dt)
	
	x[a] = c.x



plt.plot(t,x)
plt.show()

