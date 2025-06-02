#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:16:29 2024

@author: diegop
"""
from datetime import datetime, timedelta

def parameters_list(lines):
    # initialize lists
    ID_num = []
    center_x = []
    center_y = []
    angle = []
    date_time = []
    CPU_temp = []

    for line in lines:
        # replace unnecessary characters in line
        line = line.replace('[','')
        line = line.replace(']','')
        line = line.replace('CPU','')
        
        # replace month name with month number so that it can be converted to datetime type
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for month in range(0,len(months)):
            line = line.replace(months[month],str(month+1))
            
        # split line by spaces
        line = line.split()
        
        # extract info and convert to usable types
        ID_num.append(int(line[6]))
        center_x.append(float(line[8]))
        center_y.append(float(line[9]))
        angle.append(float(line[11]))
        CPU_temp.append(float(line[13]))
        
        # record dates and times as datetime type for calculations
        (h, m, s) = line[3].split(':')
        line_time = datetime(int(line[4]),int(line[1]),int(line[2]),int(h),int(m),int(s))
        date_time.append(line_time)
        
    return ID_num, center_x, center_y, angle, date_time, CPU_temp
    
    
    