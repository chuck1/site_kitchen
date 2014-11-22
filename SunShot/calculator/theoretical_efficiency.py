import pylab as pl
import numpy as np

q = 1e6
A = 1
s = 5.67e-8
ep = 0.95
C = 293.15

e_carnot = lambda H: 1 - C/H

e_rec = lambda H,A: 1 - A * s * ep * (H**4 - C**4) / q

e = lambda H,A: e_carnot(H) * e_rec(H,A)

H = np.arange(C, 2000)

#pl.plot(H, e_carnot(H))
#pl.plot(H, e_rec(H))

for A in [1,10,100]:
    pl.plot(H, e(H,A))


pl.set_ylim([0,1])

pl.show()

