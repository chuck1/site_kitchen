#!/usr/bin/env python3

import oodb
import sunshotdb

obj = list(oodb.DB.objects())

for o in obj:
    print(o, o.id)
    




