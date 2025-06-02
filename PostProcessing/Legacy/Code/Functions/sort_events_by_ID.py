#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:48:15 2024

@author: diegop
"""
from enter_or_exit_vector import * 
from enter_or_exit_y import *


from datetime import timedelta

def sort_events_by_ID(ID_num, center_x, center_y, angle, detections_by_ID, max_ID):
    # initialize data variable
    events_by_ID = []

    max_event_duration = 60 # max amount of time (in seconds) that can pass between
                                    # detections with the same ID before a new event is recorded
                                    ### $ can change this time if you want
    threshold = 30 # the minimum angle (in degrees) away from the x-axis in any
                           # direction that must be reached by the summed
                           # vector direction to reasonably estimate "enter" or "exit"
                           ### $ can change this time if you want

    # create an event list for each ID
    for ID in range(0,max_ID+1):
        events_by_ID.append([])
        
    for m in range(0,len(detections_by_ID[0:max_ID+1])):
        
        if detections_by_ID[m] == []:
            # if an ID's list of detections is empty, return string saying so
            events_by_ID[m] = 'no detections for this ID'
            
        else:
            
            event = 0 # initialize index for sorted_data

            
            for detection in range(0,len(detections_by_ID[m])):
                
                if detection == 0: # if first detection, automatically append entry info
                    angles_temp = [] # initialize list of angles for event for enter_or_exit_vector() function
                    detections_index = [] # Initialize list of detection index for entire event
                    
                    angles_temp.append(detections_by_ID[m][detection][3]) # append first event's first angle
                    detections_index.append(detections_by_ID[m][detection][5]) # append first event's first angle
                    
                    center_x_start = detections_by_ID[m][detection][1] # retrieve event's first detection x location
                    center_y_start = detections_by_ID[m][detection][2] # retrieve event's first detection y location
                    time_start = detections_by_ID[m][detection][4] # retrieve event's first detection time
                    ID_num_index = detections_by_ID[m][detection][5] # retrieve event's starting index within ID_num
                    
                    events_by_ID[m].append([]) # add sublist to populate
                    events_by_ID[m][event].append(ID_num_index) # append event's starting index within ID_num
                    events_by_ID[m][event].append(time_start) # append event's start time
                    
                elif detection < len(detections_by_ID[m])-1 and detections_by_ID[m][detection][4]-detections_by_ID[m][detection-1][4] <= timedelta(seconds=max_event_duration):
                    
                    angles_temp.append(detections_by_ID[m][detection][3]) # append event's next angle
                    detections_index.append(detections_by_ID[m][detection][5]) # append detection index for current event
                    
                elif detections_by_ID[m][detection][4]-detections_by_ID[m][detection-1][4] > timedelta(seconds=max_event_duration): # if detection is not first or last
                    
                    event += 1 # go to next index for sorted_data
                
                    # create new event if more than max_event_duration has passed
                    # if detections_by_ID[m][detection+1][4]-detections_by_ID[m][detection][4] > timedelta(seconds=max_event_duration):
                        
                    # record exit info for last event
                    center_y_end = detections_by_ID[m][detection-1][2] # retrieve event's last detection location
                    center_x_end = detections_by_ID[m][detection-1][1] # retrieve event's last detection location
                    time_end = detections_by_ID[m][detection-1][4] # retrieve event's last detection time
                    ID_num_index = detections_by_ID[m][detection-1][5]
                        
                    events_by_ID[m][event-1].append(ID_num_index) # append event's ending index within ID_num
                    events_by_ID[m][event-1].append(time_end) # append event's end time
                    events_by_ID[m][event-1].append(enter_or_exit_y(center_y_start,center_y_end)) # append event type estimated using location
                    events_by_ID[m][event-1].append(enter_or_exit_vector(angles_temp,threshold)) # append event type estimated using summed vector direction
                    
                    events_by_ID[m][event-1].append(detections_index)   
                    # record entry info for this event
                    center_y_start = detections_by_ID[m][detection][2]
                    center_x_start = detections_by_ID[m][detection][1]
                    time_start = detections_by_ID[m][detection][4]
                    ID_num_index = detections_by_ID[m][detection][5]
                        
                    events_by_ID[m].append([])
                    events_by_ID[m][event].append(ID_num_index)
                    events_by_ID[m][event].append(time_start)
                        
                    angles_temp = []
                    angles_temp.append(detections_by_ID[m][detection][3]) # append event's next angle   
                    
                    detections_index = []
                    detections_index.append(detections_by_ID[m][detection][5]) # append detection index for current event

                if detection == len(detections_by_ID[m])-1: # if detection is last, automatically append exit info
                    angles_temp.append(detections_by_ID[m][detection][3]) 
                    center_y_end = detections_by_ID[m][detection][2]
                    center_x_end = detections_by_ID[m][detection][1]
                    time_end = detections_by_ID[m][detection][4]
                    ID_num_index = detections_by_ID[m][detection][5]
                    
                    # sorted_data[event].append(center_y_end)
                    events_by_ID[m][event].append(ID_num_index)
                    events_by_ID[m][event].append(time_end)
                    events_by_ID[m][event].append(enter_or_exit_y(center_y_start,center_y_end))
                    events_by_ID[m][event].append(enter_or_exit_vector(angles_temp,threshold))
                    events_by_ID[m][event].append(detections_index)
                 
    return events_by_ID
