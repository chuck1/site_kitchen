import sys

import oodb

s0 = 'oodb.class_util.designs'
s0 = 'oodb.class_util.experiments'

s1 = "'id', ('type',lambda x: str(type(x))), 'Re', 'desc', 'mdot'"

s1 = "'id', ('design',lambda s: s.geo.design), 'Re', "
s1 = "'receiver_efficiency', ('dp/L3', lambda x: x.get('dp') / x.get('length')**3)"
s1 = "'id', 'desc', 'width'"
s1 = "'id', 'desc', 'mass_flow_rate', 'pressure_drop'"

def main():    
        app = oodb.gui.spreadsheet.Application(sys.argv)
        w = oodb.gui.spreadsheet.Window(s0,s1)
        sys.exit(app.exec_())

if __name__ == '__main__':

        
        main()
