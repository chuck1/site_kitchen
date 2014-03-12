
from multiprocessing import Process, Pipe

import time

def f2():
	for it in range(3):
		time.sleep(1)


def f(p,conns):
	for it in range(3):

		time.sleep(1)
	
		for c in conns:
			c.send([p])
			print p, " receiving ",c.recv()
		
	


c12,c21 = Pipe()
c23,c32 = Pipe()
c13,c31 = Pipe()

p = [0]*3

p[0] = Process(target=f, args=(1,(c12,c13)))
p[1] = Process(target=f, args=(2,(c21,c23)))
p[2] = Process(target=f, args=(3,(c31,c32)))

for P in p:
	P.start()

for P in p:
	P.join()


for P in p:
	f2()


