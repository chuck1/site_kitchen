# read all objects into a single list

import pylab as pl

import oodb

db = oodb.DB()

db.display(
    oodb.class_util.designs,
    ['id', 'desc', ('type', type)])

##for o in oodb.class_util.rectangulars(db.lst):
##    o.display()


##db.change_type(13, oodb.classes.Rectangular)
##db.change_type(15, oodb.classes.Rectangular)
##db.change_type(17, oodb.classes.Rectangular)
##db.change_type(19, oodb.classes.Rectangular)
##db.change_type(21, oodb.classes.Rectangular)
##
##db.change_type(30, oodb.classes.PinFin)
##db.change_type(32, oodb.classes.PinFin)
##db.change_type(34, oodb.classes.PinFin)
##db.change_type(36, oodb.classes.PinFin)
##db.change_type(38, oodb.classes.PinFin)
##db.change_type(40, oodb.classes.PinFin)
##db.change_type(42, oodb.classes.PinFin)
##db.change_type(44, oodb.classes.PinFin)
##db.change_type(46, oodb.classes.PinFin)
##db.change_type(48, oodb.classes.PinFin)


##db.save()




db.display(
    oodb.class_util.simulations,
    ['Re', 'dp'])


