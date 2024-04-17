#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:38:33 2024

@author: diegop
"""
# =============================================================================
# Sort detections by ID
# =============================================================================



def sort_detect_by_ID(ID_num, center_x, center_y, angle, date_time, CPU_temp, max_ID):
    # initalize data variable
    detections_by_ID = []

    # create a detection list for each ID
    for ID in range(0,max_ID+1):           ### instead max(ID_num) replace by max_ID othersiwe in case of a false ID with large number the list can be unnecessary long
        detections_by_ID.append([])
       
    # populate each ID's list with its detections
    for k in range(0,max_ID+1):
        if ID_num[k] <= max_ID:
            detections_by_ID[ID_num[k]].append([ID_num[k],center_x[k],center_y[k],angle[k],date_time[k],k])
        
    
    return detections_by_ID