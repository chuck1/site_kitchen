#!/usr/bin/env python

import csv

def app(l, v):
    if v:
        if not v in l:
            l.append(v)

locations = []

with open('log.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print row
        
        app(locations, row[0])
        app(areas    , row[1])
        app(walls    , row[2])



