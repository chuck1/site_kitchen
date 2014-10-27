# read all objects into a single list


import oodb

db = oodb.DB()

g = oodb.class_util.all

db.display(
    g,
    ['id', 'desc'])


