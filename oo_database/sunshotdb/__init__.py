
import os
import sys

import oodb

import sunshotdb.models

oodb.NAME = 'sunshotdb'

oodb.ROOT,_ = os.path.split(__file__)

oodb.DB = oodb.Database()

