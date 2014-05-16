import numpy as np
import pylab as pl
import math

def linear(x1,x2,y1,y2,goal):
	m = (y2-y1)/(x2-x1)
	b = y2 - m * x2
	x = (goal - b) / m
	return x

def log(x1,x2,y1,y2,goal):
	
	m = (np.log(y2) - np.log(y1)) / (np.log(x2) - np.log(x1))
	b = np.log(y2) - m * np.log(x2)
	x = (np.log(goal) - b) / m
	return np.exp(x)
	
	

# @param x1 initial guess
# @param x2 initial guess
# @param f function f(x)=0
def shooting(obj,x,f,goal):
	print "shooting method"
	
	# x[0] and x[1] are the two initial guesses

	goal = np.array(goal)

	print "x",x
	print "f",f
	print "goal",goal
	print "shape(goal)",np.shape(goal)
	#print type(goal)
	#print goal

	

		
	X = np.zeros((2,) + np.shape(goal))
	
	#print np.shape(X)
	#print np.shape(X[0])
	
	X[0] = np.ones(np.shape(goal)) * x[0]
	X[1] = np.ones(np.shape(goal)) * x[1]

	

	Y = np.zeros((2,) + np.shape(goal))

	Y[0] = f(obj,X[0])
	Y[1] = f(obj,X[1])
	
	#print "X",X
	#print "Y",Y
	#print "loop"

	i = 0
	j = 1
	
	for a in range(3):
		
		xn = log(X[j], X[i], Y[j], Y[i], goal)
		yn = f(obj,xn)
		
		"""
		if xn < 0:
			break
		if math.isinf(xn):
			break
		if math.isinf(yn):
			break
		"""
		
		def plot():
			print X
			print Y
			pl.plot(X,Y,'o')
			pl.loglog(X,Y,'o')
			pl.show()
		#plot()
	
		
		print X,np.shape(X)
		print Y,np.shape(Y)
		print xn,np.shape(xn)
		print yn,np.shape(yn)
		
		#X = np.append(X, np.reshape(xn, (1,) + np.shape(xn)), 0)
		X = np.append(X, np.reshape(xn, (1,) + np.shape(xn)), 0)
		#Y = np.append(Y, np.reshape(yn, (1,) + np.shape(yn)), 0)
		Y = np.append(Y, np.reshape(yn, (1,)), 0)

		if(np.all(np.fabs(Y[-1] - goal) < 1.0)):
			break
		
		#d1 = math.fabs(X[-1] - X[j])
		#d2 = math.fabs(X[-1] - X[i])
		
		#if(d1 < d2):
		#	i = j
		#else:
		#	i = i

		i = j
		j = j + 1
	

	
	#i = x > 0
	#x = x[i]
	#y = y[i]

	#print x
	#print y

	#y = y + 1e5

	def plot():
		pl.plot(X,Y,'o')
		pl.loglog(X,Y,'o')
		pl.show()
	#plot()

	#print X

	return X[-1]












