#!/usr/bin/env python
import sys
import numpy as np

"""
(haynes230 solid
        (chemical-formula . #f)
            (density (constant . 8970))
            (specific-heat (polynomial 2075.20411065008 -4.478165333273548 0.007790720700722077 -5.624953256013382e-06 1.49543331781846e-09))
            (thermal-conductivity (polynomial 8.4 0.02))
            )
"""

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('property')
    parser.add_argument('-T', type=float, help='temperature')
    args = parser.parse_args()


    if args.property == 'thermal_conductivity':

        if not args.T:
            print 'temperature required'
            sys.exit(1)
        
        print np.polyval([0.02, 8.4], args.T)
        
        sys.exit(0)


    if args.property in ['specific_heat', 'cp']:

        if not args.T:
            print 'temperature required'
            sys.exit(1)

        p_cp = [1.49543331781846e-09, -5.624953256013382e-06, 0.007790720700722077, -4.478165333273548, 2075.20411065008]

        #2075.20411065008, -4.478165333273548, 0.007790720700722077, -5.624953256013382e-06, 1.49543331781846e-09
        
        print np.polyval(p_cp, args.T)
        
        sys.exit(0)

    if args.property == 'density':

        print 8970

        sys.exit(0)

    print 'unknown property'

    sys.exit(1)
    

