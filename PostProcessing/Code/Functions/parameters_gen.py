#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:26:38 2024

@author: diegop
"""

# This is knows as an "empty" class that can be used to store a group of variables 
# inside and object (in this case "p") of the class Parameters

class Parameters:
    pass

def parameters_gen():
    
    # Definition fo the object "p"
    
    p = Parameters()
    
    # These are the variables used to for the statistical report
    
    p.percent_ID_detected, p.total_num_detections, p.total_num_events, p.total_num_detections_per_event, p.total_num_enter_events = [],[],[],[],[]
    p.total_num_exit_events, p.total_num_unknown_events, p.total_percent_enter, p.total_percent_exit, p.total_percent_unknow = [],[],[],[],[] 
    p.total_num_trips, p.percent_events_for_trips, p.total_avg_trip_length_s, p.total_avg_trip_length_stdev = [],[],[],[] 
    p.total_avg_trip_length_time, p.total_avg_event_length_time, p.total_avg_event_length_time_std, p.tag_IDs_per_colony = [],[],[],[]
    p.max_trip_len_sec, p.num_trips_less_than = [], []
    return p
    



