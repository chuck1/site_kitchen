
class Design:
    def __init__(self, i):
        self.id = i

    def resolve(self, lst):
        pass

class Geo:
    def __init__(self, i):
        self.id = i

    def resolve(self, lst):
        self.design = oodb.util.get_object(lst, self.design_id)

class Simulation:
    def __init__(self, i):
        self.id = i

        self.temp_heated = 0.0

    def receiver_efficiency(self):
        emis = 0.95
        
        radi = 5.67e-8 * 0.95 * (pow(self.temp_heated, 4) - pow(298.0, 4))

        conv = 15.0 * (self.temp_heated - 298.0)
        
        return self.design.qpp * emis / (self.design.qpp + radi + conv)

    def resolve(self, lst):
        print('resolve')
        self.geo = oodb.util.get_object(lst, self.geo_id)





