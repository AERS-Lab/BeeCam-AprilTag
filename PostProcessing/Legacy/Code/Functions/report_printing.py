#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:19:48 2024

@author: diegop
"""

import statistics
from datetime import timedelta

def report_printing(min_ID, max_ID, detections_by_ID,events_by_ID, trips_by_ID, all_trips_sec):
    # %%===========================================================================
    # Calculate statistics
    # =============================================================================

    # percent of IDs that were detected
    count_ID_detected = 0
    for ID in detections_by_ID[min_ID:max_ID+1]:
        if ID != []:
            count_ID_detected +=1
    proportion_ID_detected = count_ID_detected / (max_ID-min_ID+1)
    print('Percentage of IDs that were detected =','%2.f' % (proportion_ID_detected*100),'%')

    # total number of detections (without false detections)
    num_detections = 0
    for ID in detections_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            num_detections += len(ID)
    print('Total number of detections (not including false detections) =',num_detections)

    # number of false detections
    false_detections = []
    for ID in range(0,len(detections_by_ID)):
        if ID < min_ID or ID > max_ID:
            for detection in range(0,len(detections_by_ID[ID])):
                false_detections.append(detections_by_ID[ID][detection])
    false_detection_IDs = []
    for detection in false_detections:
        false_detection_IDs.append(detection[0])
    print('There were',len(false_detections),'false detections with IDs:',false_detection_IDs)
            
    # total number of identified events (without false detections)
    num_events = 0
    for ID in events_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            num_events += len(ID)
    print('Total number of events =',num_events)

    # average number of detections per event
    print('Avg num detections per event =', '%.2f' % (num_detections/num_events))

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
    proportion_enter = num_enter_events/num_events
    proportion_exit = num_exit_events/num_events
    proportion_unknown = num_unknown_events/num_events
    print()
    print('%.2f' % (proportion_enter*100),'% of events were enter (both methods agree), or a total of',num_enter_events)
    print('%.2f' % (proportion_exit*100),'% of events were exit (both methods agree), or a total of',num_exit_events)
    print('%.2f' % (proportion_unknown*100),'% of events were unknown, or a total of',num_unknown_events)

    # number of trips
    num_trips = 0
    for ID in trips_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID' and ID != 'no clear trips for this ID':
            num_trips += len(ID)
    print()
    print(num_trips,'trips were identified')

    # proportion of events that were used to identify trips
    proportion_events_for_trips = num_trips*2 / num_events # num_trips*2 because each trip used 2 events
    print('Percentage of events that were used to identify trips =','%.2f' % (proportion_events_for_trips*100),'%')

    # average trip length
    avg_trip_length_s = statistics.mean(all_trips_sec)
    avg_trip_length_stdev = statistics.stdev(all_trips_sec)
    avg_trip_length_time = timedelta(seconds=round(avg_trip_length_s))
    print('Avg trip length (in seconds) =', '%.2f' % avg_trip_length_s, 'with std dev =', '%.2f' % avg_trip_length_stdev)
    print('Avg trip length (in hh:mm:ss) =', avg_trip_length_time, 'with std dev =', timedelta(seconds=round(avg_trip_length_stdev)))

    # average event length
    event_lengths = []
    for ID in events_by_ID[min_ID:max_ID+1]:
        if ID != 'no detections for this ID':
            for event in ID:
                event_length = event[3] - event[1]
                event_lengths.append(event_length.total_seconds())
    avg_event_length_s = statistics.mean(event_lengths)
    avg_event_length_stdev = statistics.stdev(event_lengths)
    avg_event_length_time = timedelta(seconds=round(avg_event_length_s))
    print('Avg event length =','%.2f' % avg_event_length_s,'seconds with std dev =','%.2f' % avg_event_length_stdev)


    return