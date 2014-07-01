#!/usr/bin/env python

import numpy as np
import math
import argparse
import scipy.optimize

parser = argparse.ArgumentParser()
parser.add_argument('-p',action='store_true')
args = parser.parse_args()

if args.p:
    import pylab as pl

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

# x1 = PT
# x2 = D
# y = f
def fitfun(p, x1, x2):
    #return p[0] * np.power(x1, p[1]) * np.power(x2, p[2])
    return p[0] * x1**p[1] * x2**p[2]
    
def errfun(p, x1, x2, z_meas):
    return (fitfun(p, x1, x2) - z_meas)




print A
print Y

X = np.linalg.solve(A,Y)

print X

xd = np.power(PT,X[1]) * np.power(D,X[2])


xl = np.linspace(np.min(xd),np.max(xd),100)
fl = math.exp(X[0]) * xl



#p0 = [1e-8, 3.0, -2.0]
p0 = [math.exp(X[0]), X[1], X[2]]

#p = scipy.optimize.leastsq(errfun, p0, args=(PT, D, f))
p = scipy.optimize.leastsq(errfun, p0, args=(PT[:3], D[:3], f[:3]))



def plot():
    fig = pl.figure()
    ax = fig.add_subplot(111)

    ax.plot(xd,f,'o')

    ax.plot(xl,fl,'-')

    pl.show()

err1 = errfun(p[0], PT, D, f)
err2 = errfun(p0, PT, D, f)

print "f   =",f
print "k   =",math.exp(X[0])
print "a   =",X[1]
print "b   =",X[2]
print "p0  =",p0
print "p   =",p[0]
print "err =",err1
print "%err=",err1 / f * 100.0
print "err =",err2
print "%err=",err2 / f * 100.0




