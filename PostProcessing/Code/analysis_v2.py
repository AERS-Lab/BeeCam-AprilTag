#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:28:31 2024

@author: diegop
"""
import sys
import os
sys.path.append(os.path.abspath("./Functions")) ## Adds the path of the folder Functions
from parameters_list import *
from sort_detect_by_ID import *
from sort_events_by_ID import *
from sort_trips_by_ID import *
from csv_events import *
from plot_generator import *
#from Functions import  parameters_list, sort_detect_by_ID, sort_events_by_ID



# =============================================================================
# Load data
# =============================================================================

# set min and max ID
min_ID = 0 # $ change this to smallest tag ID number used, if necessary
max_ID = 99 # $ change this to highest tag ID number used, if necessary

# read .txt file
with open('../Data/queen.txt') as file: # $ change file name if necessary
    lines = file.readlines()
    file.close()
    
# Extract parameters from data file

ID_num, center_x, center_y, angle, date_time, CPU_temp = parameters_list(lines)

# Sort detections by ID numbers

detections_by_ID = sort_detect_by_ID(ID_num, center_x, center_y, angle, date_time, CPU_temp, max_ID)

# Identify events by ID numbers

events_by_ID = sort_events_by_ID(ID_num, center_x, center_y, angle, detections_by_ID, max_ID)

# Estimate Trips by ID

trips_by_ID = sort_trips_by_ID(events_by_ID)

# Genarate a CSV file that contains the events by ID number

csv_events(events_by_ID)

# generates and save plots in the Results folder

plot_generator(trips_by_ID, ID_num, max_ID, min_ID, events_by_ID)




