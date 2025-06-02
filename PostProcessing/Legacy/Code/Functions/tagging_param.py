#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:03:34 2024

@author: diegop
"""
import csv
from datetime import datetime

# create an object for each queen and worker with attributes of date, tags and notes.

class hives_info:
    pass

def tagging_param():
    # create object "q" that contains tagging parameters 
    q = hives_info()
    
    csv_file = open('../Tagging_info.csv', 'r')
    
    # skip first line
    csv_file.readline()
    
    q.RPid = []
    q.hiveNo = []
    q.date = []
    q.TagStart = []
    q.TagStop = []
    q.TotalTags = []
    q.notes = []
    
    
    for a, b, c, d, e, f, g in csv.reader(csv_file, delimiter=','):
        q.RPid.append(a)
        q.hiveNo.append(b)
        q.date.append(datetime.strptime(c, '%m/%d/%y'))
        q.TagStart.append(d)
        q.TagStop.append(e)
        q.TotalTags.append(f)
        q.notes.append(g)
        
    
    return q



