#!/usr/bin/env python3
import oodb
import sunshotdb

d = oodb.DB.get_object(116)

g = sunshotdb.models.Geo(oodb.util.get_next_id(oodb.ROOT), d.id)

g.data['desc'] = "full design; halfed by symmetry"

o = sunshotdb.models.Simulation(oodb.util.get_next_id(oodb.ROOT), g.id)

print(g,g.id)
print(o,o.id)

o.data['desc'] = 'sim#0004 conjugate fluent full design'
o.data['pressure_inlet'] = 4.45E4
o.data['pressure_channel_inlet'] = 3.14E4
o.data['pressure_channel_outlet'] = 1.35E4
o.data['pressure_outlet'] = 0.0
o.data['temperature_inlet'] = 773.1
o.data['temperature_outlet'] = 918.1
o.data['temperature_channel_inlet'] = 807
o.data['temperature_channel_outlet'] = 901

oodb.util.save_to_next(oodb.ROOT, [g,o])

