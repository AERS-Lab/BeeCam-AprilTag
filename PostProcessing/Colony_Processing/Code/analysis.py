#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:28:31 2024

@author: diegop
"""
import sys
import os
sys.path.append(os.path.abspath("./Functions")) ## Adds the path of the folder Functions
from parameters_gen import *
from parameters_list import *
from sort_detect_by_ID import *
from sort_events_by_ID import *
from sort_trips_by_ID import *
from csv_events import *
from plot_generator import *
from report_printing import *
from report_gen2 import *
from csv_report import *
#from Functions import  parameters_list, sort_detect_by_ID, sort_events_by_ID


#%%
# =============================================================================
# Load data
# =============================================================================


# read .txt file

# Type the name of the Colony like: queen, worker01, worker02, ....
colony = 'queen'
# introduce the Min and Max ID numbers tagged
min_ID = 0
max_ID = 299

# Call class to define variables inside object p
p = parameters_gen()

    
with open('../Data/' + colony + '.txt') as file: # $ change file name if necessary 
    lines = file.readlines()
    file.close()
        
    # Extract parameters from data file

ID_num, center_x, center_y, angle, date_time, CPU_temp = parameters_list(lines)

    # Sort detections by ID numbers

detections_by_ID = sort_detect_by_ID(ID_num, center_x, center_y, angle, date_time, CPU_temp, max_ID)

    # Identify events by ID numbers

events_by_ID = sort_events_by_ID(ID_num, center_x, center_y, angle, detections_by_ID, max_ID)

    # Estimate Trips by ID

trips_by_ID, all_trips, all_trips_sec = sort_trips_by_ID(events_by_ID)

    # Genarate a CSV file that contains the events by ID number

csv_events(colony, events_by_ID)

    # generates and save plots in the Results folder

plot_generator(colony, trips_by_ID, ID_num, max_ID, min_ID, events_by_ID, all_trips_sec)

    ## Report summary

    #report_printing(min_ID, max_ID, detections_by_ID,events_by_ID, trips_by_ID, all_trips_sec)
    #
p = report_gen2(colony, min_ID, max_ID, detections_by_ID, events_by_ID, trips_by_ID, all_trips_sec, p)


    #
csv_report(colony, p)


#%%


