#!/usr/bin/env python

import signal
import sys
import re
import argparse
import subprocess
import myos
import shutil
import os

devnull = open(os.devnull)

process = None
filename_modified = None

def test(filename, makefile, target_filename):
    global process
    global filename_modified

    print filename
    
    with open(filename, 'r') as f:
        lines = f.readlines()
  
    #print lines

    inc_line_ind = []

    # identify all lines with include directives
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

        m = re.search("#include <(.*)>", l)
        if not m:
            print "failed to get header name"
            print l
            sys.exit(1)
        
        header_filename = m.group(1)
        if target_filename:
            if header_filename == target_filename:
                pass
            else:
                print "skip: {}".format(header_filename)
                continue
        
        shutil.copy(filename, filename + '.original')
   
        lines_copy[ind] = '//' + lines_copy[ind][:-1] + ' removed by c_header_checker\n'
        
        with open(filename, 'w') as f:
            f.writelines(lines_copy)
        
        filename_modified = filename

        #print lines,lines_copy
        
        out = []
        
        
        
        process = subprocess.Popen(['make','-f',makefile,'-j4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #ret = subprocess.call(['make'], stdout=subprocess.DEVNULL, stderr=devnull)
        #ret = subprocess.Popen(['make'], stdout=out, stderr=devnull)
        
        print "building..."
        out, err = process.communicate()
        print "build complete"
       
        process = None

        #print "out,err"
        #print repr(out),repr(err)

        if not err:
            print repr(l), "in file", repr(filename), "can be removed"
        else:
            print repr(err)
            shutil.move(filename + '.original', filename)

        filename_modified = None

# command lnie args
parser = argparse.ArgumentParser(description="identify and remove unneccesary include directives in a C/C++ project")
parser.add_argument('makefile')
parser.add_argument('-f', help="specify header file")
parser.add_argument('-d', help="root directory", default=".")
parser.add_argument('-v', help="verbosity", action="store_true")
args = parser.parse_args()

if args.v:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

def signal_handler(signal, frame):
    print 'you pressed ctrl+c'

    if process:
        print 'terminate process'
        process.terminate()
    if filename_modified:
        print "restore: {}".format(filename_modified)
        shutil.move(filename_modified + '.original', filename_modified)

    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

c_files = myos.glob(".*\.cpp$", args.d)
h_files = myos.glob(".*\.hpp$", args.d)

logging.debug("\n".join(c_files))
logging.debug("\n".join(h_files))

for c in c_files:
    test(c, args.makefile, args.f)

for h in h_files:
    test(h, args.makefile, args.f)



