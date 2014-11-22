import pylab as pl
import numpy as np

s = 5.67e-8
C = 293.15
#A = 1
#R = (A * s * ep * C**4) / q

def R(d):
    ep = d['ep']
    qpp = d['qpp']
    return (s * ep * C**4) / (qpp)

e_carnot = lambda H: 1 - C/H

e_rec = lambda H, R, ep: ep - R * (H**4 - C**4) / C**4

e = lambda H, R, ep: e_carnot(H) * e_rec(H,R,ep)

H = np.arange(C, 3000)

#pl.plot(H, e_carnot(H))
#pl.plot(H, e_rec(H))

leg = []

def plot(string, values):
    for value in values:
        d = {
                'ep': 0.9,
                'qpp': 1e6}
        d[string] = value
        
        pl.plot(H, e(H, R(d), d['ep']))
        leg.append(str(d))
    


plot("qpp",[1e6,2e6,3e6])
plot("ep",[0.5,0.7,0.9])

pl.ylim([0,1])
pl.legend(leg, loc=2)

pl.show()



