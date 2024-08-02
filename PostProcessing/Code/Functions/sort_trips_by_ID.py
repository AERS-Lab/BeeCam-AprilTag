#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:15:51 2024

@author: diegop
"""

# =============================================================================
# Process data: determine trips
# =============================================================================
    
def sort_trips_by_ID(events_by_ID):

    trips_by_ID = []

    for ID in range(0,len(events_by_ID)):
        prev_event = 'initial'
        
        if events_by_ID[ID] == 'no detections for this ID':
            trips_by_ID.append('no detections for this ID')
            
        else:
            trips_by_ID.append([]) # create new list for new ID
            
            for event in range(0,len(events_by_ID[ID])): # go through each event for an ID
               
                if events_by_ID[ID][event][4] == events_by_ID[ID][event][5][0]: 
                    # if both methods of determining an event agree, can use for determining a trip
                    current_event = events_by_ID[ID][event][4]
                elif events_by_ID[ID][event][4] == 'unknown' and events_by_ID[ID][event][5][0] == 'enter':
                    current_event = 'enter'
                elif events_by_ID[ID][event][4] == 'unknown' and events_by_ID[ID][event][5][0] == 'exit':
                    current_event = 'exit'    
                else:
                    current_event = 'NA'
                    
                if current_event == 'enter' and prev_event == 'exit': 
                    # if bee is entering after exiting, call it a trip
                    exit_time = events_by_ID[ID][event-1][3]
                    enter_time = events_by_ID[ID][event][1]
                    trip_time =  enter_time - exit_time
                    trip_time_sec = int(trip_time.total_seconds())
                    trips_by_ID[ID].append([exit_time,enter_time,trip_time, trip_time_sec]) # add trip to ID
                    
                prev_event = current_event # set previous event for next loop
                
            if trips_by_ID[ID] == []: 
                # if no trips were identified (even though there were detections), say that
                trips_by_ID[ID] = 'no clear trips for this ID'
    
    all_trips = []

    for ID in range(0,len(trips_by_ID)):
        if trips_by_ID[ID] != 'no detections for this ID' and trips_by_ID[ID] != 'no clear trips for this ID' and trips_by_ID[ID] != 'only one detection for this ID':
            for trip in range(0,len(trips_by_ID[ID])):
                all_trips.append(trips_by_ID[ID][trip][2])

    all_trips_sec = []
    for time in all_trips:
        all_trips_sec.append(int(time.total_seconds()))
        
    return trips_by_ID, all_trips, all_trips_sec
    