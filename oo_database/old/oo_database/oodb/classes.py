import oodb.util

class Design:
    def __init__(self, i):
        self.id = i

    def resolve(self, db):
        pass

class Geo:
    def __init__(self, i, design_id):
        self.id = i
        self.design_id = design_id

    def resolve(self, db):
        self.design = db.get_object(self.design_id)

class Simulation:
    def __init__(self, i, geo_id):
        self.id = i
        self.geo_id = geo_id

        self.temp_heated = 0.0

    def receiver_efficiency(self):
        emis = 0.95
        
        radi = 5.67e-8 * 0.95 * (pow(self.temp_heated, 4) - pow(298.0, 4))

        conv = 15.0 * (self.temp_heated - 298.0)
        
        return self.design.qpp * emis / (self.design.qpp + radi + conv)

    def resolve(self, db):
        self.geo = db.get_object(self.geo_id)






