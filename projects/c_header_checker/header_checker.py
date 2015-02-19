#!/usr/bin/env python

import argparse
import subprocess
import myos
import shutil
import os

devnull = open(os.devnull)

def test(filename, makefile):
    
    print filename

    with open(filename, 'r') as f:
        lines = f.readlines()
  
    #print lines

    inc_line_ind = []
    
    a = 0
    for l in lines:
        if l[:8] == '#include':
            #print repr(l)
            #l = "//" + l
            inc_line_ind.append(a)
            #print repr(l[10:-2])
        a += 1
        
    print inc_line_ind

    for ind in inc_line_ind:

        lines_copy = list(lines)

        l = lines_copy[ind]

        shutil.copy(filename, filename + '.original')
   
        lines_copy[ind] = '//' + lines_copy[ind][:-1] + ' removed by c_header_checker\n'

        with open(filename, 'w') as f:
            f.writelines(lines_copy)

        #print lines,lines_copy

        out = []

        p = subprocess.Popen(['make','-f',makefile,'-j4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #ret = subprocess.call(['make'], stdout=subprocess.DEVNULL, stderr=devnull)
        #ret = subprocess.Popen(['make'], stdout=out, stderr=devnull)
        
        out, err = p.communicate()
       
       
        #print "out,err"
        #print repr(out),repr(err)

        if not err:
            print repr(l), "in file", repr(filename), "can be removed"
        else:
            print repr(err)
            shutil.move(filename + '.original', filename)

parser = argparse.ArgumentParser()
parser.add_argument('makefile')
args = parser.parse_args()

c_files = myos.glob(".*\.cpp$")

for c in c_files:
    test(c, args.makefile)

h_files = myos.glob(".*\.hpp$")

for h in h_files:
    test(h, args.makefile)



