import numpy as np
import pylab as pl




def plot_ctrl_attitude(c):
	fig = pl.figure()
	
	ax = fig.add_subplot(111)
	ax.set_ylabel('tau_RB')

	ax.plot(c.c.t, c.tau_RB)
	
	
	fig = pl.figure()
	
	ax = fig.add_subplot(221)
	ax.set_ylabel('e_1')
	ax.plot(c.c.t, c.e1)

	ax = fig.add_subplot(222)
	ax.set_ylabel('e_2')
	ax.plot(c.c.t, c.e2)



