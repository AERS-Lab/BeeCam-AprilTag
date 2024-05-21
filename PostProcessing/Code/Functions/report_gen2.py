#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:47:12 2024

@author: diegop
"""
import statistics
from datetime import timedelta

def report_gen2(colony, min_ID, max_ID, detections_by_ID, events_by_ID, trips_by_ID, all_trips_sec, p):
    # ===========================================================================
    # Calculate statistics
    # =============================================================================
    print('=========================================================')
    print('Statistics for "' + colony + '" ' )
    print('=========================================================')
    print('')
    # Tagging ID numbers range
    ID_range = str(min_ID) + ' - ' + str(max_ID)
    p.tag_IDs_per_colony.append(ID_range)

    # percent of IDs that were detected
    count_ID_detected = 0
    for ID in detections_by_ID[min_ID:max_ID+1]:
        if ID != []:
            count_ID_detected +=1
    
    p.percent_ID_detected.append((count_ID_detected / (max_ID-min_ID+1)*100))

    print('Percentage of IDs that were detected =','%2.f' % (p.percent_ID_detected[0]),'%')

    # total number of detections (without false detections)
    num_detections = 0
    
    for ID in detections_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            num_detections += len(ID)

    p.total_num_detections.append(num_detections)
    print('Total number of detections (not including false detections) =',p.total_num_detections[0])

    # number of false detections
    false_detections = []
    for ID in range(0,len(detections_by_ID)):
        if ID < min_ID or ID > max_ID:
            for detection in range(0,len(detections_by_ID[ID])):
                false_detections.append(detections_by_ID[ID][detection])
    false_detection_IDs = []
    for detection in false_detections:
        false_detection_IDs.append(detection[0])
    #print('There were',len(false_detections),'false detections with IDs:',false_detection_IDs)
            
    # total number of identified events (without false detections)
    num_events = 0
    
    for ID in events_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            num_events += len(ID)

    p.total_num_events.append(num_events)
    print('Total number of events =',p.total_num_events[0])

    
    if p.total_num_detections[0] > 0 and p.total_num_events[0] > 0:
        
        p.num_detections_per_event = p.total_num_detections[0]/p.total_num_events[0]
        p.total_num_detections_per_event.append(p.num_detections_per_event)
    else:
        p.total_num_detections_per_event.append("NaN")
        
    # average number of detections per event
    print('Avg num detections per event =', '%.2f' % (p.total_num_detections_per_event[0]))

    # of identified events, proportion that were enter
    num_enter_events = 0
    num_exit_events = 0
    num_unknown_events = 0

    

    for ID in events_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            for event in ID:
                if event[4] == 'enter' and event[5][0] == 'enter':
                        num_enter_events += 1
                elif event[4] == 'exit' and event[5][0] == 'exit':
                        num_exit_events += 1
                else:
                    num_unknown_events += 1

    p.total_num_enter_events.append(num_enter_events)
    p.total_num_exit_events.append(num_exit_events)
    p.total_num_unknown_events.append(num_unknown_events)

    if num_events > 0:
        proportion_enter = num_enter_events/num_events
        proportion_exit = num_exit_events/num_events
        proportion_unknown = num_unknown_events/num_events
    else:
        proportion_enter = 0
        proportion_exit = 0
        proportion_unknown = 0

    

    p.total_percent_enter.append(proportion_enter*100)
    p.total_percent_exit.append(proportion_exit*100)
    p.total_percent_unknow.append(proportion_unknown*100)

    print()
    print('%.2f' % (p.total_percent_enter[0]),'% of events were enter (both methods agree), or a total of',p.total_num_enter_events[0])
    print('%.2f' % (p.total_percent_exit[0]),'% of events were exit (both methods agree), or a total of',p.total_num_exit_events[0])
    print('%.2f' % (p.total_percent_unknow[0]),'% of events were unknown, or a total of',p.total_num_unknown_events[0])

    # number of trips
    num_trips = 0
    for ID in trips_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID' and ID != 'no clear trips for this ID':
            num_trips += len(ID)
    
    p.total_num_trips.append(num_trips)

    print()
    print(num_trips,'trips were identified')

    # proportion of events that were used to identify trips
    if num_events > 0:
        proportion_events_for_trips = num_trips*2 / num_events # num_trips*2 because each trip used 2 events
    else:
        proportion_events_for_trips = 0
    
    p.percent_events_for_trips.append(proportion_events_for_trips*100)
    print('Percentage of events that were used to identify trips =','%.2f' % (proportion_events_for_trips*100),'%')

    
    # average trip length
    #### Function to return trips less than certain period
    max_trip_len_sec = 7200
    
    def smaller_than(sequence, value):
        return [item for item in sequence if item < value]
    
    all_trips_sec_lessthan = smaller_than(all_trips_sec, max_trip_len_sec)


    if len(all_trips_sec_lessthan) > 0:    
        avg_trip_length_s = statistics.mean(all_trips_sec_lessthan)
        avg_trip_length_stdev = statistics.stdev(all_trips_sec_lessthan)
        avg_trip_length_time = timedelta(seconds=round(avg_trip_length_s))
    else:
        avg_trip_length_s = 0
        avg_trip_length_stdev = 0
        avg_trip_length_time = 0

    p.total_avg_trip_length_s.append(avg_trip_length_s)
    p.total_avg_trip_length_stdev.append(str(timedelta(seconds=round(avg_trip_length_stdev))))
    p.total_avg_trip_length_time.append(str(avg_trip_length_time))
    
    print('For trips less than ' + str(max_trip_len_sec) +'s = '+ str(round(max_trip_len_sec/60)) + 'min' )
    print('Avg trip length (in seconds) =', '%.2f' % avg_trip_length_s, 'with std dev =', '%.2f' % avg_trip_length_stdev)
    print('Avg trip length (in hh:mm:ss) =', avg_trip_length_time, 'with std dev =', timedelta(seconds=round(avg_trip_length_stdev)))

    # average event length
    all_events_lengths = []
    #event_lengths = []
    event_list = []
    for ID in events_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            for event in ID:
                event_list.append(event)
                event_length = event[3] - event[1]
                all_events_lengths.append(event_length.total_seconds())
                
                
    ## Extract events greater than Min=0 seconds and less than Max=120 seconds 
    
    def limit_event(sequence, Min, Max):
        return [ item for item in sequence if item < Max and item > Min ]
    event_lengths = limit_event(all_events_lengths, 0, 120)
    
    
    if len(event_lengths) > 1:
        avg_event_length_s = statistics.mean(event_lengths)
        avg_event_length_stdev = statistics.stdev(event_lengths)
    elif len(event_lengths) == 1:
        avg_event_length_s = event_lengths[0]
        avg_event_length_stdev = event_lengths[0]
    else:
        avg_event_length_s = 0
        avg_event_length_stdev = 0
        
    avg_event_length_time = timedelta(seconds=round(avg_event_length_s))
    avg_event_length_time_std = timedelta(seconds=round(avg_event_length_stdev))

    

    p.total_avg_event_length_time.append(str(avg_event_length_time))
    p.total_avg_event_length_time_std.append(str(avg_event_length_time_std))


    print('Avg event length =','%.2f' % avg_event_length_s,'seconds with std dev =','%.2f' % avg_event_length_stdev)
    
    print('---------------------------------------------------------')
op    print('')
    print('')



    return p
