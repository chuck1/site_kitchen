import math

# stress in pin

#known

fluid_pressure = 10 * 1e5

D = 7e-4
PT = 5

# calc

PL = math.sqrt(3)/2.0 * PT

ST = PT*D
SL = PL*D

area_pin = math.pi * D**2 / 4.0
area_fluid = ST * SL - area_pin

stress_pin = area_fluid / area_pin * fluid_pressure




# stress concentration

C = 1.4

stress_max = C * stress_pin





print "stress_pin {0:f} MPa".format(stress_pin/1e6)
print "stress_max {0:f} MPa".format(stress_max/1e6)

