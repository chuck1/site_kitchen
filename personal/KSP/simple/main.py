#!/usr/bin/env python

from celestialbodies import *

import kerbaltime

class Mission:
	def __init__(self):
		pass

destination = Eve

o1 = Orbit(Kerbin, 700E3, 0, 0, 0, 0, 0, 0)

mission = Mission()

mission.transferType = "optimal"
mission.originBody = Kerbin

initialOrbitalVelocity = o1.speedAtTrueAnomaly(0)

finalOrbitalVelocity = destination.circularOrbitVelocity(100e3)

t0 = kerbaltime.KerbalTime(0)
dt = kerbaltime.fromDuration(5)



# transferType, originBody, destinationBody, t0, dt, initialOrbitalVelocity, finalOrbitalVelocity, p0, v0, n0, p1, v1, planeChangeAngleToIntercept
t = transfer("optimal", mission.originBody, Eve, t0.t, dt.t, initialOrbitalVelocity, finalOrbitalVelocity)

td = transferDetails(t, mission.originBody, t0, mission.initialOrbitalVelocity);

print transfer


