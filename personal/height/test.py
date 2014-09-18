#!/usr/bin/env python

import math
from matplotlib import cm as cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from height import *

def grad(X,Y,Z):
    dx = X[0,1]-X[0,0]
    G = np.gradient(Z,dx)
    g = np.sqrt(np.square(G[0]) + np.square(G[1]))
    
    g = g-np.min(g)
    g = g/np.max(g)
    
    return g

def plot(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    c = ax.contourf(X, Y, Z, 10)
    plt.colorbar(c)
    
    plt.show()

def plot3(X,Y,Z):
    fig = plt.figure()
    ax = Axes3D(fig)
   
    G = grad(X,Y,Z)
    
    ax.plot_surface(X, Y, Z,  rstride=1, cstride=1, facecolors=cm.jet(G))
    
    plt.show()


def cylinder(Z):
    x = np.linspace(0,2*math.pi,nx)
    y = np.linspace(0,10,ny)
    
    X, Y, Z, uX, uY, uZ = cylinder(x,y,1)
    Z = perturb(X,Y,Z,uX,uY,uZ,pZ,nx,ny)

    plot(X,Y,Z)

def plane(Z):
    s = np.shape(Z)
    nx = s[0]
    ny = s[1]
    x = np.linspace(0,10,nx)
    y = np.linspace(0,10,ny)
    
    X,Y = np.meshgrid(x,y)

    return X,Y
   
nx = 100
ny = 100

Z = np.random.random_sample((nx,ny))
#Z = np.random.rand(nx,ny)
#Z = np.zeros((nx,ny))

X,Y = plane(Z)

Z = filtw(Z,20)

#Z = crater(X,Y,Z,5,5,2,0.4)

#Z = filt(Z,5)

#Z = norm(Z)

#Z = below(Z,0.5)

plot(X,Y,Z)

#plot3(X,Y,Z)



#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='RdBu', linewidth=0, antialiased=False)


