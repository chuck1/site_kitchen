import sys
import os
import numpy as np
import csv

module_dir = os.environ["HOME"] + "/Programming/Python/Modules/"
sys.path.append(module_dir)

def read(filename):
	with open( filename, 'rb' ) as f:
		reader = csv.reader( f, quoting=csv.QUOTE_NONNUMERIC )
		
		# skip first line
		
		
		rows=[]

		r = 0
		while 1:
			try:
				rows.append( reader.next() )
				
				r += 1
			except ValueError:
				#print "ValueError"
				continue
			except:
				#print sys.exc_info()[0]
				break
			
		
	return np.array( rows )
	

