# create a new object and add it to the database

import oodb

d = oodb.classes.Design(oodb.util.get_next_id())

d.desc = 'high aspect; rectangular'

d.fluid_str = 'co2'
d.qpp = 1e6
d.temp_in = 773.15
d.temp_out = 923.15

d.height_channel = 4e-5
d.width_channel = 1e-3
d.width_wall = 1e-4
d.length_channel = 6.6e-3
d.length_in = 8e-5
d.length_out = 8e-5
d.height_front = 1e-4
d.height_back = 1e-4

g = oodb.classes.Geo(oodb.util.get_next_id(), d.id)

g.desc = 'half channel'

g.number_of_channels_modeled = 0.5
g.v_in = 4.99

oodb.util.save_to_next([d,g])

