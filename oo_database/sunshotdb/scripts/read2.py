#!/usr/bin/env python3

import oodb
import sunshotdb

#obj = list(oodb.DB.objects())

obj = list(oodb.DB.objects(objtype=sunshotdb.models.Rectangular))

for o in obj:
    print(o, o.id)
    pass



