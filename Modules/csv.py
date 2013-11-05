import sys
import time
import math
from multiprocessing import Process, Queue
import os
import re
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('/nfs/stak/students/r/rymalc/Documents/python')

class Object_csv_line:
	def __init__( self, lines ):
		self.lines = lines
		self.col = 0
		self.row = 0
		self.data = np.array( [] )

	def run(self):
		row = len(self.lines)
		col = 1
		
		self.data = np.zeros( ( row, col ) )
		
		for a in range(0,row):
			#print 'line=%r' % line
			
			s = re.split('\s*,\s*',self.lines[a])
			
			c = len(s)
			
			#print "s",s
			while c > col:
				data_add = np.zeros( ( row, 1 ) )
				self.data = np.append( self.data, data_add, axis=1 )
				col += 1
			
			for b in range(0,c):
				#f = float( s[b].strip() )
				#print "f",f
				
				#print "a",a,"b",b
				
				self.data[a,b] = float( s[b].strip() )

		self.row = row
		self.col = col	


def process_csv_line(object,q):
	print "process id:", os.getpid()
	object.run()
	q.put([object])


def read_csv(filename):
	f = open(filename,'r')

	# skip first line
	iterf = iter(f)
	next(iterf)

	lines = [] #np.array([])

	# file length
	print "grabing lines..."
	
	for line in iterf:
		lines.append(line)
	
	l = len(lines)
	
	print "%i lines" % l

	# number of threads
	n = int( math.ceil( float(l)/70000.0 ) )
	
	print "processing in %i threads" % n
	
	lst = 0
	nxt = l/n
	
	start_time = time.time()
	
	threads = [0]*n
	processes = [0]*n
	queues = [0]*n
	for a in range(0,n):
		print "thread %i: lines %i through %i" % ( a, lst, nxt )
		queues[a] = Queue()
		
		threads[a] = Object_csv_line( lines[ lst:nxt ] )
		
		processes[a] = Process( target=process_csv_line, args=( threads[a], queues[a], ) )
		processes[a].start()
		
		lst = nxt
		if a == n-2:
			nxt = l
		else:
			nxt = nxt + l/n
		
	# join threads and find maximum number of columns
	col = 0
	for a in range(0,n):
		q = queues[a].get()

		threads[a] = q[0]

		processes[a].join()
		
		if threads[a].col > col:
			col = threads[a].col

	duration = time.time() - start_time

	# equalize number of columns
	data_add = np.zeros( ( threads[a].row, 1 ) )
	
	for a in range(0,n):
		while threads[a].col < col:
			threads[a].data = np.append( threads[a].data, data_add, axis=1 )
			threads[a].col += 1
	
	# combine data

	data = threads[0].data
	
	for a in range(1,n):
		data = np.append( data, threads[a].data, axis=0 )
	
	#duration = time.clock() - start_time

	print "elapsed time: %f seconds" % duration
	#print "shape(data)",np.shape(data)
	return data











