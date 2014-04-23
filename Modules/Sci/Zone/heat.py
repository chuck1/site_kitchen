import numpy as np

def cross_flow_tube_bank_staggered(Re,Pr):
	
	if np.all(Re >= 10) and np.all(Re <= 1e2):
		C = 0.9
		m = 0.4
	else:
		raise 0
	
	
	Nu = C * np.power(Re, m) * np.power(Pr, 0.36)
	
	return Nu


