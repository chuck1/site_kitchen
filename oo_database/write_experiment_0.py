# create a new object and add it to the database

import oodb



d = oodb.classes.Design(oodb.util.get_next_id())



e = oodb.classes.Experiment(oodb.util.get_next_id(), d)






oodb.util.save_to_next([d,e])

