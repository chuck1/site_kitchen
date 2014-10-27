import math
import inspect

import oodb.util
import Fluids

class FluidSettings:
    def __init__(self, string):
        if string == 'co2':
            self.qpp        = 1e6
            self.temp_in    = 773.15
            self.temp_out   = 923.15
        if string == 'ms':
            self.qpp        = 4e6
            self.temp_in    = 573.15
            self.temp_out   = 873.15
            
class Object:

    def print_dict(self):
        print('__dict__:')
        for k,v in self.__dict__.items():
            print(k,v)

    def get(self, name):
        #print('get')

        a = getattr(self, name)

        if inspect.ismethod(a):
            #print('method', a())
            return a()
        else:
            #print('not method')
            return a

class Design(Object):
    def __init__(self, i):
        print('Design.__init__')
        self.id = i

    def resolve(self, db):
        print('Design.resolve')
        try:
            self.fluid = Fluids.Fluid(self.fluid_str)
            self.fs = FluidSettings(self.fluid_str)
        except:
            self.print_dict()
            print('__dict__:')
            for k,v in self.__dict__.items():
                print(k,v)
                
    def display(self):
        for k,v in self.__dict__.items():
            print(k,v)

    def Re(self):
        
        T = self.temp_avg()
        
        rho = self.fluid.get('density', T)
        mu = self.fluid.get('viscosity', T)
        
        return rho * self.D_h() * self.v() / mu

    def temp_avg(self):
        return (self.temp_in + self.temp_out) / 2.0

    def v(self):
        rho = self.fluid.get('density', self.temp_avg())
        return self.mdot() / rho / (self.A_cs() * self.get('NT'))

    # total mass flow rate for device
    def mdot(self):
        dh = self.fluid.enthalpy_change(self.temp_in, self.temp_out)
        return self.qpp * self.A_heated() / dh

    # 
    def A_heated(self):
        return self.get('width') * self.get('length')
    
    
    
class Rectangular(Design):
    def __init__(self, i):
        Design.__init__(self, i)

    def width(self):
        return self.width_channel + self.width_wall

    def length(self):
        return self.length_channel

    def D_h(self):
        
        P = 2.0 * (self.width_channel + self.height_channel)
        return 4 * self.A_cs() / P

    def NT(self):
        return (self.get('width') - self.width_channel) / (self.width_channel + self.width_wall) + 1

    def A_cs(self):
        return self.width_channel * self.height_channel

class PinFin(Design):
    def __init__(self, i):
        Design.__init__(self, i)

    def width(self):
        return self.ST * self.NT + 2.0 * self.SE

    def length(self):
        return self.SL * self.NL

    def D_h(self):
        return self.D

    def gap(self):
        return self.D - self.ST

    def A_cs(self):
        return math.pi * self.gap()**2 / 4.0


### Geo

class Geo:
    def __init__(self, i, design_id):
        self.id = i
        self.design_id = design_id

    def resolve(self, db):
        self.design = db.get_object(self.design_id)

### Simulation

class Simulation(Object):
    def __init__(self, i, geo_id):
        self.id = i
        self.geo_id = geo_id

    def length(self):
        return self.geo.design.get('length')

    def receiver_efficiency(self):
        emis = 0.95
        
        radi = 5.67e-8 * 0.95 * (pow(self.temp_heated_awa, 4) - pow(298.0, 4))

        conv = 15.0 * (self.temp_heated_awa - 298.0)
        
        return self.geo.design.qpp * emis / (self.geo.design.qpp + radi + conv)

    def resolve(self, db):
        self.geo = db.get_object(self.geo_id)


    def Re(self):
        return self.geo.design.Re()


## Experiment

class Experiment(Object):
    def __init__(self, i, design_id):
        self.id = i
        self.design_id = design_id

    def resolve(self, db):
        self.design = db.get_object(self.design_id)

    def length(self):
        return self.design.get('length')



