# create a new object and add it to the database

from util import *
from classes import *

s = Simulation(8)
s.desc = 'hello'

replace(s, 8)

