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
n = [nx,ny,nz]

prob = solver.prob.Problem('opt1', X, n, it_max_1 = 1000, it_max_2 = 1000)

prob.create_equation('T', 10.0, 1.5, 1.5)
prob.create_equation('s', 10.0, 1.5, 1.5)

s = 1.0e10

# patch groups

g_hi_xp		= prob.create_patch_group('hi_xp', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_yp		= prob.create_patch_group('hi_yp', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_ym		= prob.create_patch_group('hi_ym', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_zo		= prob.create_patch_group('hi_zo', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_zi		= prob.create_patch_group('hi_zi', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

g_ho_xp		= prob.create_patch_group('ho_xp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_yp		= prob.create_patch_group('ho_yp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_ym		= prob.create_patch_group('ho_ym',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_zo		= prob.create_patch_group('ho_zo',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_zi		= prob.create_patch_group('ho_zi',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

g_pi		= prob.create_patch_group('pi',		v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_po		= prob.create_patch_group('po',		v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

g_ch_xp		= prob.create_patch_group('ch_xp', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ch_yp		= prob.create_patch_group('ch_yp', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ch_ym_i	= prob.create_patch_group('ch_ym_i', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ch_ym_o	= prob.create_patch_group('ch_ym_o', v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

# inlet
f_hi_xp   = g_hi_xp.create_patch('f_hi_xp',	1, [3,		[0,1,2,3],	[0,1,2,3]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_hi_yp_1 = g_hi_yp.create_patch('f_hi_yp_1',	2, [[1,2,3],	3,		[0,1,2,3]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_hi_yp_o = g_hi_yp.create_patch('f_hi_yp_o',	2, [[0,1],	3,		[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_hi_yp_i = g_hi_yp.create_patch('f_hi_yp_i',	2, [[0,1],	3,		[2,3]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_hi_ym   = g_hi_ym.create_patch('f_hi_ym',	-2,[[3,2,1,0],	0,		[3,2,1,0]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_hi_zo   = g_hi_zo.create_patch('f_hi_zo',	-3,[[3,2,1,0],	[3,2,1,0],	0],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_hi_zi_1 = g_hi_zi.create_patch('f_hi_zi_1',	3, [[2,3],	[0,1,2,3],	3],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_hi_zi_2 = g_hi_zi.create_patch('f_hi_zi_2',	3, [[0,1,2],	[0,1],		3],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_hi_zi_3 = g_hi_zi.create_patch('f_hi_zi_3',	3, [[0,1,2],	[2,3],		3],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# outlet
f_ho_xp   = g_ho_xp.create_patch('f_ho_xp',	1, [3,		[0,1,2,3],	[6,7,8,9]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_ho_yp_1 = g_ho_yp.create_patch('f_ho_yp_1',	2, [[1,2,3],	3,		[6,7,8,9]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ho_yp_o = g_ho_yp.create_patch('f_ho_yp_o',	2, [[0,1],	3,		[8,9]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ho_yp_i = g_ho_yp.create_patch('f_ho_yp_i',	2, [[0,1],	3,		[6,7]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_ho_ym   = g_ho_ym.create_patch('f_ho_ym',-2, [[3,2,1,0],	0,		[9,8,7,6]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_ho_zo   = g_ho_zo.create_patch('f_ho_zo', 3, [[0,1,2,3],	[0,1,2,3],	9],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_ho_zi_1 = g_ho_zi.create_patch('f_ho_zi_1',-3, [[3,2],	[3,2,1,0],	6],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ho_zi_2 = g_ho_zi.create_patch('f_ho_zi_2',-3, [[2,1,0],	[1,0],		6],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ho_zi_3 = g_ho_zi.create_patch('f_ho_zi_3',-3, [[2,1,0],	[3,2],		6],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# channel
# need bc with heated!!!
f_ch_xp   = g_ch_xp.create_patch('f_ch_xp',	1, [2,		[1,2],	[3,4,5,6]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ch_yp   = g_ch_yp.create_patch('f_ch_yp',	2, [[0,1,2],	2,	[3,4,5,6]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ch_i_ym = g_ch_ym_i.create_patch('f_ch_i_ym',-2, [[2,1,0],	1,	[4,3]],			v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_ch_o_ym = g_ch_ym_i.create_patch('f_ch_o_ym',-2, [[2,1,0],	1,	[6,5]],			v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})


# pipe
f_pi_xp = g_pi.create_patch('f_pi_xp', 1, [1,		[3,4],	[1,2]],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_pi_zi = g_pi.create_patch('f_pi_zi', 3, [[0,1],	[3,4],	2],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_pi_zo = g_pi.create_patch('f_pi_zo',-3, [[1,0],	[4,3],	1],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

f_po_xp = g_po.create_patch('f_po_xp', 1, [1,		[3,4],	[7,8]],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_po_zi = g_po.create_patch('f_po_zi',-3, [[1,0],	[4,3],	7],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
f_po_zo = g_po.create_patch('f_po_zo', 3, [[0,1],	[3,4],	8],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

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


def solve_with_source():
	prob.solve2(1e-4, 1e-2, True)
	prob.solve('s', 1e-2, True)
	prob.value_add('s', -1.0)
	prob.value_normalize('s')
	prob.copy_value_to_source('s','T')
	prob.solve2('T', 1e-2, 1e-2, True)


prob.solve('T', 1e-2, True)

#prob.save()

#prob.plot('T')

prob.write('T')


