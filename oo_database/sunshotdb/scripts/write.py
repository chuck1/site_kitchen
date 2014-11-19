#!/usr/bin/env python3
import oodb
import sunshotdb

o = sunshotdb.models.PinFin(oodb.util.get_next_id(oodb.ROOT))

print(o)
print(o.id)

o.D = 7E-4
o.PT = 1.5

o.test()

oodb.util.save_to_next(oodb.ROOT, [o])

