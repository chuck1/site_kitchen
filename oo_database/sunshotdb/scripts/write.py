#!/usr/bin/env python3
import oodb
import sunshotdb

g = oodb.DB.get_object(145)

o = sunshotdb.models.Simulation(oodb.util.get_next_id(oodb.ROOT), g.id)

print(g,g.id)
print(o)
print(o.id)

o.data['desc'] = 'simulation number unknown'

#oodb.util.save_to_next(oodb.ROOT, [o])

