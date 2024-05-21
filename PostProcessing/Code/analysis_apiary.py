#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:28:31 2024

@author: diegop
"""
import sys
import os
sys.path.append(os.path.abspath("./Functions")) ## Adds the path of the folder Functions
from tagging_param import *
from parameters_gen import *
from parameters_list_crop_by_datetime_2 import *
from sort_detect_by_ID import *
from sort_events_by_ID import *
from sort_trips_by_ID import *
from csv_events import *
from plot_generator import *
from report_printing import *
from report_gen_colony import *
from csv_report_apiary import *
#from Functions import  parameters_list, sort_detect_by_ID, sort_events_by_ID


#%%
# =============================================================================
# Load data
# =============================================================================

#Tagging parameters are store in the object "q"
q = tagging_param()

# Insert week for analysis, choose number from 1 to 9 
week = 1

# First ID number for each colony must be written for each colony, this numbers are used as example
colony_ID = ['queen', 6000, 'worker01', 1000, 'worker02', 2000, 'worker03', 3000, 'worker04', 4000, 'worker05', 5000]

# Generate output parameters for final report  and store them inside the object "p"
p = parameters_gen()

# Empty list of tagging parameters for General Report
start_datetime =[]
stop_datetime = []
total_datetime = []
tagged_id = []

for x in range(0, len(colony_ID), 2):
    colony = colony_ID[x]
    min_ID = colony_ID[x + 1] + (week-1)*100
    max_ID = colony_ID[x + 1] + (week-1)*100 + 199
    
    with open('../Data/' + colony + '.txt') as file: # $ change file name if necessary
        lines = file.readlines()
        file.close()
    index = int(x/2)     
    crop_date = q.date[index]    
    # Extract parameters from data file

    ID_num, center_x, center_y, angle, date_time, CPU_temp = parameters_list_crop_by_datetime_2(lines, crop_date)

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
    p = report_gen_colony(colony, week, min_ID, max_ID, detections_by_ID, events_by_ID, trips_by_ID, all_trips_sec, p)
    
    ### append the start and stop date time for each colony
    start_datetime.append(crop_date.strftime('%m/%d/%Y  %H:%M:%S'))
    stop_datetime.append(date_time[-1].strftime('%m/%d/%Y  %H:%M:%S'))
    # calculate the total period of detections for processing
    total_datetime.append(str(date_time[-1] - crop_date).replace(',', ' '))
    # obtain the ID numbers range
    tagged_id.append(q.TagStart[index] + ' - ' + q.TagStop[index])


# Report generator for all colonies in the apiary
csv_report_apiary(week, colony, p, start_datetime, stop_datetime, total_datetime, tagged_id)


#%%


