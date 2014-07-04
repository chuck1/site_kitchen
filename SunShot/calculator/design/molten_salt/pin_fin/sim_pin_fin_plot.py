import pylab as pl
import numpy as np
import math

PT = np.array([
        1.5,
        1.5,
        2.0,
        2.0
        ])

RE = np.array([
        18.9,
        18.9,
        12.6,
        12.6
        ])

D = np.array([
        1.88e-4,
        2.50e-4,
        1.88e-4,
        2.50e-4
        ])

f = np.array([
        17.8,
        9.3,
        46.5,
        27.7
        ])


def plot1():
    fig = pl.figure()
    ax = fig.add_subplot(121)

    ax.plot(PT,f,'o')

    ax = fig.add_subplot(122)
    ax.plot(RE,f,'o')


#pl.show()

A = np.ones((4,3))

A[:,1] = np.log(PT)
#A[:,2] = np.log(RE)
A[:,2] = np.log(D)

Y = np.log(f)

A = A[:3,:]
Y = Y[:3]


print A
print Y

X = np.linalg.solve(A,Y)

print X

xd = np.power(PT,X[1]) * np.power(D,X[2])


xl = np.linspace(np.min(xd),np.max(xd),100)
fl = math.exp(X[0]) * xl



fig = pl.figure()
ax = fig.add_subplot(111)

ax.plot(xd,f,'o')

ax.plot(xl,fl,'-')

pl.show()


print "k =",math.exp(X[0])
print "a =",X[1]
print "b =",X[2]






