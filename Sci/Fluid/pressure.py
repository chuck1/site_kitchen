import math

# known

# need corrent numbers
rho = 1000
dh = 1e5
mu = 1e-5

# have corrent numbers
flux = 4e6
L = 1e-2
W = 1e-2


# independent variables
ST = 400e-6
D = 200e-6



# calc

SL = ST * math.sqrt(3) / 2.0

NT = W / ST
NL = W / SL

gap = ST - D

area_flow = math.pi * gap**2

mass_flow = flux * L * W / dh


v = mass_flow / rho / area_flow

Re = rho * area_flow * v / mu

f = 64.0 / Re

dp = NL * f * rho * v**2 / 2.0

print "ST        {0} m".format(ST)
print "SL        {0} m".format(SL)
print "mass_flow {0} kg/s".format(mass_flow)
print "velocity  {0} m/s".format(v)
print "pressure  {0} bar".format(dp/100000)
print "Re        {0}".format(Re)

