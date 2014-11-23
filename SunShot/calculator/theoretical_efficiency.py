import subprocess
import os
import sys
import pylab as pl
import numpy as np

s = 5.67e-8
C = 293.15
#A = 1
#R = (A * s * ep * C**4) / q


def root(C, K):
    #print('root K',K)
    r = np.roots([-4.0 * K / C**4, 3.0 * K / C**3, 0.0, 0.0, 0.0, (1 + K) * C])
    r = np.real(r[np.imag(r)==0])
    r = r[0]
    return r

vroot = np.vectorize(root)

def get_K(qpp):
    return np.divide(s * C**4, qpp)

e_carnot = lambda H: 1 - C/H

e_rec = lambda H, K, ep: ep * ( 1.0 - K * ( (H/C)**4 - 1 ) )

e = lambda H, K, ep: e_carnot(H) * e_rec(H,K,ep)


pl.rc('text', usetex=True)
pl.rc('font', family='monospace')
pl.rc('font', family='sans-serif')

fileroot = "/home/chuck/git/thesis/Media/image/background/theory/efficiency/"

def line_temp_vs_eta():

    H = np.arange(C, 2500)

    qpp = 1e6
    ep = 1.0
    
    K = get_K(qpp)
    
    pl.plot(H, e_carnot(H), 'k-')
    pl.plot(H, e_rec(H, K, ep), 'k--')
    pl.plot(H, e(H, K, ep), 'k-.')
    
    pl.ylim([0,1])
    
    pl.legend(['carnot','rec','overall'], loc=0)
   
    pl.xlabel(r"$T_H$ (K)")
    pl.ylabel(r"$\eta$")

    save("temp_vs_eta.png")

    pl.show()

def save(filename):
    pl.savefig(filename)
    subprocess.call(["cp", filename, os.path.join(fileroot, filename)])

def cont():

    f1 = pl.figure()
        
    a1 = f1.add_subplot(111)
   
    qpp = np.logspace(5, 8, 100)
    ep = np.linspace(0.5, 1.0, 100)
    
    print(np.shape(qpp))
    print(np.shape(ep))

    QPP, EP = np.meshgrid(qpp, ep)
    
    K = get_K(QPP)
    
    print(np.shape(K))
    #print('K',K)
    
    
    H = vroot(C, K)
    
    eta = e(H, K, EP)
    
    cs1 = a1.contour(np.log10(K), EP, eta, 10, colors='k')
    
    #qpp_str = r"$log(q''_{\textrm{inc}})$ (W/m$^2$)"

    pl.xlabel(r"log(K)")
    pl.ylabel(r"$\epsilon$")
    
    pl.clabel(cs1)
 
    save("cont.png")

    pl.show()

def line_logK_vs_temp():
    
    qpp = np.logspace(5, 8, 100)
        
    K = get_K(qpp)
    
    H = vroot(C, K)
    
    pl.plot(np.log10(K), H, 'k')
   
    pl.xlabel(r"log(K)")
    pl.ylabel(r'$T_H$ (K)')

    save("logK_vs_temp.png")

    pl.show()



line_temp_vs_eta()
cont()
line_logK_vs_temp()



