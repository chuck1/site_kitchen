#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


def integrate( x0, x1, y0, y1, a, b, c ):
        S = a / 3.0*( pow(x1,3) - pow(x0,3) )*( y1 - y0 ) - b / 3.0*( x1 - x0 )*( pow(y1,3) - pow(y0,3) ) + c * ( x1 - x0 ) * ( y1 - y0 )

        return S

def scale( S, x0, x1, y0, y1, a, b ):
	S0 = integrate(x0,x1,y0,y1,a,b,0)

	c = ( S - S0 ) / ( x1 - x0 ) / ( y1 - y0 )

        return c

def parab_2d_coeff_from_meas( peak, edge, edge_x ):
	a = ( edge - peak ) / edge_x / edge_x

        return a


#float vmax[3]; float vmin[3]; float vrng[3];
#centroid_stats( t, vmax, vmin, vrng );

vmax = [1e-2, 0, 1e-2]
vmin = [-1e-2, 0, 0]
vrng = [2e-2, 0, 1e-2]

# peak at center
xc = ( vmax[0] - vmin[0] ) / 2.0;

# peak at edge
zc = vmax[2];

c = 1.3e6
e = 0.7e6

# curvature based on measured peak and edge values
a = parab_2d_coeff_from_meas( c, e, vrng[0] / 2.0 )
b = a;

# initial ingeral
S0 = integrate( (vmin[0]-xc), (vmax[0]-xc), (vmin[2]-zc), (vmax[2]-zc), a, b, c )

# desired integrated value
S = 1e6 * vrng[0] * vrng[2];


# adject peak to give desired integral value
c = scale( S, (vmin[0]-xc), (vmax[0]-xc), (vmin[2]-zc), (vmax[2]-zc), a, b )

S1 = integrate( (vmin[0]-xc), (vmax[0]-xc), (vmin[2]-zc), (vmax[2]-zc), a, b, c )



print "S0={0}".format(S0)
print "S1={0}".format(S1)




x = np.arange(100) / 99.0 * vrng[0] + vmin[0]
z = np.arange(100) / 99.0 * vrng[2] + vmin[2]

X,Z = np.meshgrid(x,z)

s = a*X*X + b*Z*Z + c

CS = plt.contourf(X,Z,s)
CB = plt.colorbar(CS,format='%e')
plt.show()

