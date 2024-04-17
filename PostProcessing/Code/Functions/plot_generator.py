#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:26:43 2024

@author: diegop
"""
import matplotlib
matplotlib.use('Agg')    #### This line blocks the displaying of plottings
import matplotlib.pyplot as plt

def plot_generator(trips_by_ID, ID_num, max_ID, min_ID, events_by_ID):
    
    # =============================================================================
    # Plot trip length distribution
    # =============================================================================
    all_trips = []
    for ID in range(0,len(trips_by_ID)):
        if trips_by_ID[ID] != 'no detections for this ID' and trips_by_ID[ID] != 'no clear trips for this ID' and trips_by_ID[ID] != 'only one detection for this ID':
            for trip in range(0,len(trips_by_ID[ID])):
                all_trips.append(trips_by_ID[ID][trip][2])

    all_trips_sec = []
    for time in all_trips:
        all_trips_sec.append(int(time.total_seconds()))
        
    # initialize plot
    #fig, ax = plt.subplots()
    fig1 = plt.figure(1)
    plt.figure(figsize=(20, 12))

    # set bin ticks and labels
    num_bins = 30
    time_ticks = [] # initialize ticks
    time_labels = [] # initialize tick labels
    # max_tick = max(all_trips_sec) + (500 - (max(all_trips_sec) % 500))
    max_tick = 7200 # 2 hours
    # bin_width = int(max_tick / num_bins)
    bin_width = 120 # 2 minutes

    for n in range(0,max_tick+bin_width,bin_width):
        time_ticks.append(n)
        
        h = int( (n - n % 3600) / 3600 )
        t_left = n - h*3600
        m = int( (t_left - t_left % 60) / 60 )
        t_left = t_left - m*60
        s = int(t_left)
        
        minute_integer = int(n/60)
        
        if n % 180 == 0: # only show labels for every 6 minutes (to avoid crowding of labels)
            # time_labels.append(str(h)+':'+str(m)+':'+str(s))
            time_labels.append(str(minute_integer))
        else:
            time_labels.append('')
        
    plt.hist(all_trips_sec, bins=num_bins, range=(0,7201), color='#ff9514')
    plt.grid(which='major',axis='y', linestyle='-')
    plt.grid(which='major',axis='x', linestyle='-', color = '#ededed')

    # set bin ticks and labels
    plt.xticks(ticks=time_ticks, labels=time_labels, fontsize=18, rotation=0)
    plt.yticks(fontsize=18)

    # set titles and axis labels
    plt.title('Distribution of Trip Lengths under 2 Hours', fontsize = 30)
    plt.xlabel('Length (minutes)', fontsize = 30)
    plt.ylabel('Frequency', fontsize = 30)
    
    
    plt.savefig('../Results/Trips_Length.png')
    
    plt.close(fig1)
    ###############################################################################################
    
    # =============================================================================
    # Plot histogram of detected IDs using raw data over entire data collection period
    # (if plot is not wanted, comment out this entire section)
    # =============================================================================

    # initialize plot
    fig2 = plt.figure(2)
    plt.figure(figsize=(20, 12))
    
    plt.hist(ID_num, bins=(max_ID-min_ID+1), range=(min_ID,max_ID+1)) # bins = # of IDs, range = (first ID, last ID+1)
    plt.grid(which='major',axis='y', linestyle='--')

    # set bin ticks and labels (show tick for every ID but label every 5th ID)
    xtick_labels = []
    for label in range(min_ID,max_ID+1):
        if label % 5 == 0:
            xtick_labels.append(label)
        elif label == max_ID: # label last ID
            xtick_labels.append(label)
        else:
            xtick_labels.append(' ')        
    plt.xticks(ticks=range(min_ID,max_ID+1),labels=xtick_labels,fontsize=10)

    # set titles and axis labels
    plt.suptitle('Frequency of Tag Detections by ID (Raw Data)', fontsize=15)
    # plt.title('From '+str(record_start_time)+' to '+str(record_end_time),fontsize=10)
    plt.xlabel('ID Number', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    
    plt.savefig('../Results/Detections_histograms.png')
    
    plt.close(fig2)
    
    # ===========================================================================
    # Plot histogram of event IDs using processed data over entire data collection period
    # (if plot is not wanted, comment out this entire section)
    # =============================================================================

    # create list with frequency of each ID's events
    event_IDs = []
    for n in range(min_ID,max_ID+1):
        if events_by_ID[n] != 'no detections for this ID':
            for o in range(0,len(events_by_ID[n])):
                event_IDs.append(n)
                
    # initialize plot
    fig3 = plt.figure(3)
    plt.figure(figsize=(20, 12))
    
    plt.hist(event_IDs, bins=(max_ID-min_ID+1), range=(min_ID,max_ID+1), color='#32ABE1')
    plt.grid(which='major',axis='y', linestyle='-')

    # set bin ticks and labels (uses same formatting as previous histogram)
    plt.xticks(ticks=range(min_ID,max_ID+1), labels=xtick_labels,fontsize=10)
    plt.yticks(fontsize=18)
    # plt.grid(b=True, which='major', axis='x', linestyle='-', color='#ededed')

    # set titles and axis labels
    plt.title('Frequency of Events by ID', fontsize=30)
    # plt.title('From '+str(record_start_time)+' to '+str(record_end_time),fontsize=10)
    plt.xlabel('ID Number', fontsize=25)
    plt.ylabel('Frequency', fontsize=25)

    plt.savefig('../Results/Events_histograms.png')
    
    plt.close(fig3)



    return