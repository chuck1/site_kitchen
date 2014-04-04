
#from solver import *
import solver.prob
from solver.patch import stitch

k = 10.0
al = 1.3
alpha_src = 1.0

n = 10

x = [[0., 1.], [0., 1.], [0., 1.]]
n = [[n+0],[n+2],[n+4]]

prob = solver.prob.Problem('test4', x, n, k, al, alpha_src, it_max_1 = 1000, it_max_2 = 500)

#prob.get_3d_axes()
#sys.exit(0)

p0 = None
p1 = None
p2 = None
p3 = None
p4 = None
p5 = None

#p0 = prob.createPatch(1,	[1,	[0,1],	[0,1]])
#p1 = prob.createPatch(2,	[[0,1],	1,	[0,1]])
p2 = prob.createPatch(3,	[[0,1],	[0,1],	1])
p3 = prob.createPatch(-1,	[0,	[1,0],	[1,0]])
p4 = prob.createPatch(-2,	[[1,0],	0,	[1,0]])
p5 = prob.createPatch(-3,	[[1,0],	[1,0],	0])



stitch(p0,p1)
stitch(p0,p2)
stitch(p0,p4)
stitch(p0,p5)

stitch(p1,p2)
stitch(p1,p3)
stitch(p1,p5)

stitch(p2,p3)
stitch(p2,p4)

stitch(p3,p4)
stitch(p3,p5)

stitch(p4,p5)



#f0 = p0.faces[0,0]
#f1 = p1.faces[0,0]
f2 = p2.faces[0,0]
f3 = p3.faces[0,0]
f4 = p4.faces[0,0]
f5 = p5.faces[0,0]



#f0.create_equ('T', 0., [[30.,0.],[0.,0.]], k, al)

#f1.create_equ('T', 0., [[30.,0.],[0.,0.]], k, al)

f2.create_equ('T', 0., [[30.,30.],[30.,30.]], k, al)

f3.create_equ('T', 0., [[30.,30.],[30.,30.]], k, al)

f4.create_equ('T', 0., [[30.,30.],[30.,30.]], k, al)

f5.create_equ('T', 0., [[30.,30.],[30.,30.]], k, al)



#prob.solve2(1e-2, 1e-4, True)
prob.solve('T', 1e-1)

#prob.plot3()

prob.plot('T')

pl.show()




