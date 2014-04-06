import numpy as np
#import time
#
#import itertools
#from pylab import plot, show, figure, contour
#import pylab as pl
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#from sympy import *
#import math
#import inspect

#spreader_test()

import solver.prob
from solver.patch import stitch

x = [0.002,  0.008, 0.005]

y = [0.0015, 0.003, 0.0015, 0.02]

z = [0.008,  0.004, 0.003, 0.002, 0.010, 0.002, 0.003, 0.004, 0.008]

x = np.cumsum(np.append([0],x))
y = np.cumsum(np.append([0],y))
z = np.cumsum(np.append([0],z))

nx = [ 4, 16, 10]
ny = [ 3,  6,  3, 20]
nz = [16,  8,  6,  4,  20, 4,  6,  8, 16]

X = [x,y,z]
N = [nx,ny,nz]

k = 10.
al = 1.4

prob = solver.prob.Problem('opt1', X, N,
		k = k,
		alpha = al,
		alpha_src = 1.4,
		it_max_2 = 20)


# inlet
f_hi_xp   = prob.createPatch('f_hi_xp', 1, [3,		[0,1,2,3],	[0,1,2,3]])

prob.patch_groups.append([f_hi_xp])

f_hi_yp_1 = prob.createPatch('f_hi_yp_1', 2, [[1,2,3],	3,		[0,1,2,3]])
f_hi_yp_o = prob.createPatch('f_hi_yp_o', 2, [[0,1],	3,		[0,1]])
f_hi_yp_i = prob.createPatch('f_hi_yp_i', 2, [[0,1],	3,		[2,3]])

prob.patch_groups.append([f_hi_yp_1, f_hi_yp_i, f_hi_yp_o])

f_hi_ym   = prob.createPatch('f_hi_ym',-2, [[3,2,1,0],	0,		[3,2,1,0]])

prob.patch_groups.append([f_hi_ym])

f_hi_zo   = prob.createPatch('f_hi_zo',-3, [[3,2,1,0],	[3,2,1,0],	0])

prob.patch_groups.append([f_hi_zo])

f_hi_zi_1 = prob.createPatch('f_hi_zi_1', 3, [[2,3],	[0,1,2,3],	3])
f_hi_zi_2 = prob.createPatch('f_hi_zi_2', 3, [[0,1,2],	[0,1],		3])
f_hi_zi_3 = prob.createPatch('f_hi_zi_3', 3, [[0,1,2],	[2,3],		3])

prob.patch_groups.append([f_hi_zi_1, f_hi_zi_2, f_hi_zi_3])

# outlet
f_ho_xp   = prob.createPatch('f_ho_xp', 1, [3,		[0,1,2,3],	[6,7,8,9]],	)

prob.patch_groups.append([f_ho_xp])

f_ho_yp_1 = prob.createPatch('f_ho_yp_1', 2, [[1,2,3],	3,		[6,7,8,9]],	)
f_ho_yp_o = prob.createPatch('f_ho_yp_o', 2, [[0,1],	3,		[8,9]],		)
f_ho_yp_i = prob.createPatch('f_ho_yp_i', 2, [[0,1],	3,		[6,7]],		)

prob.patch_groups.append([f_ho_yp_1, f_ho_yp_i, f_ho_yp_o])

f_ho_ym   = prob.createPatch('f_ho_ym',-2, [[3,2,1,0],	0,		[9,8,7,6]],	)

prob.patch_groups.append([f_ho_ym])

f_ho_zo   = prob.createPatch('f_ho_zo', 3, [[0,1,2,3],	[0,1,2,3],	9],		)

prob.patch_groups.append([f_ho_zo])

f_ho_zi_1 = prob.createPatch('f_ho_zi_1',-3, [[3,2],	[3,2,1,0],	6],		)
f_ho_zi_2 = prob.createPatch('f_ho_zi_2',-3, [[2,1,0],	[1,0],		6],		)
f_ho_zi_3 = prob.createPatch('f_ho_zi_3',-3, [[2,1,0],	[3,2],		6],		)

prob.patch_groups.append([f_ho_zi_1, f_ho_zi_2, f_ho_zi_3])

# channel
# need bc with heated!!!
f_ch_xp   = prob.createPatch('f_ch_xp', 1, [2,		[1,2],	[3,4,5,6]])

f_ch_xp.set_v_bou('T', [[2.0,2.0],[4.0,4.0]])

f_ch_yp   = prob.createPatch('f_ch_yp', 2, [[0,1,2],	2,	[3,4,5,6]])

f_ch_i_ym = prob.createPatch('f_ch_i_ym',-2, [[2,1,0],	1,	[4,3]])

f_ch_o_ym = prob.createPatch('f_ch_o_ym',-2, [[2,1,0],	1,	[6,5]])

prob.patch_groups.append([f_ch_xp])
prob.patch_groups.append([f_ch_yp])
prob.patch_groups.append([f_ch_i_ym])
prob.patch_groups.append([f_ch_o_ym])

# pipe
f_pi_xp = prob.createPatch('f_pi_xp', 1, [1,		[3,4],	[1,2]])
f_pi_zi = prob.createPatch('f_pi_zi', 3, [[0,1],	[3,4],	2])
f_pi_zo = prob.createPatch('f_pi_zo',-3, [[1,0],	[4,3],	1])

prob.patch_groups.append([f_pi_xp])
prob.patch_groups.append([f_pi_zi])
prob.patch_groups.append([f_pi_zo])

f_po_xp = prob.createPatch('f_po_xp', 1, [1,		[3,4],	[7,8]])
f_po_zi = prob.createPatch('f_po_zi',-3, [[1,0],	[4,3],	7])
f_po_zo = prob.createPatch('f_po_zo', 3, [[0,1],	[3,4],	8])

prob.patch_groups.append([f_po_xp])
prob.patch_groups.append([f_po_zi])
prob.patch_groups.append([f_po_zo])

# stitching
# inlet
stitch(f_hi_xp,   f_hi_yp_1)
stitch(f_hi_xp,   f_hi_ym)
stitch(f_hi_xp,   f_hi_zo)
stitch(f_hi_xp,   f_hi_zi_1)

stitch(f_hi_yp_1, f_hi_yp_o)
stitch(f_hi_yp_1, f_hi_yp_i)
stitch(f_hi_yp_1, f_hi_zo)
stitch(f_hi_yp_1, f_hi_zi_1)
stitch(f_hi_yp_1, f_hi_zi_3)

stitch(f_hi_yp_o, f_hi_zo)

stitch(f_hi_ym,   f_hi_zo)

stitch(f_hi_zi_1, f_hi_zi_2)
stitch(f_hi_zi_1, f_hi_zi_3)

# outlet
stitch(f_ho_xp,   f_ho_yp_1)
stitch(f_ho_xp,   f_ho_ym)
stitch(f_ho_xp,   f_ho_zo)
stitch(f_ho_xp,   f_ho_zi_1)

stitch(f_ho_yp_1, f_ho_yp_o)
stitch(f_ho_yp_1, f_ho_yp_i)
stitch(f_ho_yp_1, f_ho_zo)
stitch(f_ho_yp_1, f_ho_zi_1)
stitch(f_ho_yp_1, f_ho_zi_3)

stitch(f_ho_yp_o, f_ho_zo)

stitch(f_ho_ym,   f_ho_zo)

stitch(f_ho_zi_1, f_ho_zi_2)
stitch(f_ho_zi_1, f_ho_zi_3)

# channel
stitch(f_ch_xp, f_hi_zi_1)
stitch(f_ch_xp, f_ho_zi_1)
stitch(f_ch_xp, f_ch_yp)
stitch(f_ch_xp, f_ch_i_ym)
stitch(f_ch_xp, f_ch_o_ym)

stitch(f_ch_yp, f_hi_zi_3)
stitch(f_ch_yp, f_ho_zi_3)

stitch(f_ch_i_ym, f_hi_zi_2)
stitch(f_ch_o_ym, f_ho_zi_2)

# pipe
# -inlet
stitch(f_pi_xp, f_hi_yp_1)

stitch(f_pi_zo, f_hi_yp_o)
stitch(f_pi_zi, f_hi_yp_i)

# -outlet
stitch(f_po_xp, f_ho_yp_1)

stitch(f_po_zo, f_ho_yp_o)
stitch(f_po_zi, f_ho_yp_i)



#prob.solve2(1e-4, 1e-2, True)
prob.solve('s',1e-2)
prob.value_add('s', -1.0)
prob.value_normalize('s')

#prob.save()

ax = prob.plot('s')

pl.show()


