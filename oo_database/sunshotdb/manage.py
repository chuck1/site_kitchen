#!/usr/bin/env python3

import argparse
import readline
import code


import oodb
import sunshotdb


parser = argparse.ArgumentParser()
parser.add_argument("command")
args = parser.parse_args()




if args.command == "shell":
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

