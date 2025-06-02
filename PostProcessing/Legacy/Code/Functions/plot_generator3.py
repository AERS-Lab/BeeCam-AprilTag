#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:51:21 2024

@author: diegop
"""

import statistics as stats
import time
import matplotlib
import matplotlib.dates as mdates
from datetime import datetime, timedelta
#matplotlib.use('Agg')    #### This line blocks the displaying of plottings
import matplotlib.pyplot as plt

def plot_generator3(colony, trips_by_ID, ID_num, maxID, minID, events_by_ID, all_trips_sec2, date_time, ID_tagged):
       
    # =============================================================================
    # =============================================================================
    # Plot distribution for each ID range tagged
    # =============================================================================
    # =============================================================================
    
    
    for k in range(0, len(ID_tagged)):
        max_ID = ID_tagged[k][-1]
        min_ID = ID_tagged[k][0]
        # =============================================================================
        # Plot trip length distribution
        # =============================================================================
        all_trips_sec = []
        for ID in range(min_ID, max_ID+1):
            if trips_by_ID[ID] != 'no detections for this ID' and trips_by_ID[ID] != 'no clear trips for this ID' and trips_by_ID[ID] != 'only one detection for this ID':
                for trip in range(0,len(trips_by_ID[ID])):
                    all_trips_sec.append(trips_by_ID[ID][trip][3])
            
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
        bin_width = int(max_tick / num_bins) # bins are 4 minutes long
        #bin_width = 120 # 2 minutes
        total_trips = len(all_trips_sec)
        # all trips less than max_thick
        all_trips_sec_less_than = [x for x in all_trips_sec if x <= max_tick]
        
        for n in range(0,max_tick+bin_width,bin_width):
            time_ticks.append(n)
            
            h = int( (n - n % 3600) / 3600 )
            t_left = n - h*3600
            m = int( (t_left - t_left % 60) / 60 )
            t_left = t_left - m*60
            s = int(t_left)
            
            minute_integer = int(n/60)
            
            if n % 240 == 0: # only show labels for every 4 minutes (to avoid crowding of labels)
                # time_labels.append(str(h)+':'+str(m)+':'+str(s))
                time_labels.append(str(minute_integer))
            else:
                time_labels.append('')
            
        counts, edges, bars = plt.hist(all_trips_sec_less_than, bins=num_bins, range=(0,7201), color='#ff9514')
        plt.grid(which='major',axis='y', linestyle='-')
        plt.grid(which='major',axis='x', linestyle='-', color = '#ededed')
        plt.bar_label(bars, weight='bold')
        # set bin ticks and labels
        plt.xticks(ticks=time_ticks, labels=time_labels, fontsize=14, rotation=0)
        plt.yticks(fontsize=18)
        total_trips_less_than = int(sum(counts))
        # set titles and axis labels
        plt.title('Distribution of Trip Lengths under 2 Hours ('+str(total_trips_less_than)+' out of '+str(total_trips)+' total)', fontsize = 30)
        plt.xlabel('Length (minutes)', fontsize = 30)
        plt.ylabel('Frequency', fontsize = 30)
        # Mean plot
        mean = stats.mean(all_trips_sec_less_than)
        mean_time = time.strftime("%M:%S", time.gmtime(mean))
        plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        plt.text(mean*1.1, max_ylim*0.9, 'Mean: '+mean_time, weight='bold')
        
        # Median plot
        median = stats.median(all_trips_sec_less_than)
        median_time = time.strftime("%M:%S", time.gmtime(median))
        plt.axvline(median, color='k', linestyle='dashed', linewidth=1)
        plt.text(median*1.1, max_ylim*0.7, 'Median: ' + median_time, weight='bold')
        
        # Mode plot
        mode = stats.mode(all_trips_sec_less_than)
        mode_time = time.strftime("%M:%S", time.gmtime(mode))
        plt.axvline(mode, color='k', linestyle='dashed', linewidth=1)
        plt.text(mode*1.1, max_ylim*0.5, 'Mode: ' + mode_time, weight='bold')
        
        plt.savefig('../Results/' + colony + '_Trips_Length_IDs['+str(min_ID)+','+str(max_ID)+'].png')
        
        plt.close(fig1)
        ###############################################################################################
        
        # =============================================================================
        # Plot histogram of detected IDs using raw data over entire data collection period
        # (if plot is not wanted, comment out this entire section)
        # =============================================================================

        # initialize plot
        fig2 = plt.figure(2)
        plt.figure(figsize=(20, 12))
        
        counts_detec, edges_detect, bars_detect = plt.hist(ID_num, bins=(max_ID-min_ID+1), range=(min_ID,max_ID+1)) # bins = # of IDs, range = (first ID, last ID+1)
        plt.grid(which='major',axis='y', linestyle='--')
        plt.bar_label(bars_detect, weight='bold')
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
        
        plt.savefig('../Results/' + colony + '_Detections_histograms_IDs['+str(min_ID)+','+str(max_ID)+'].png')
        
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
        
        counts_event, edges_event, bars_event=plt.hist(event_IDs, bins=(max_ID-min_ID+1), range=(min_ID,max_ID+1), color='#32ABE1')
        plt.grid(which='major',axis='y', linestyle='-')
        plt.bar_label(bars_event, weight='bold')
        # set bin ticks and labels (uses same formatting as previous histogram)
        plt.xticks(ticks=range(min_ID,max_ID+1), labels=xtick_labels,fontsize=10)
        plt.yticks(fontsize=18)
        # plt.grid(b=True, which='major', axis='x', linestyle='-', color='#ededed')

        # set titles and axis labels
        plt.title('Frequency of Events by ID', fontsize=30)
        # plt.title('From '+str(record_start_time)+' to '+str(record_end_time),fontsize=10)
        plt.xlabel('ID Number', fontsize=25)
        plt.ylabel('Frequency', fontsize=25)

        plt.savefig('../Results/' + colony + '_Events_histograms_IDs['+str(min_ID)+','+str(max_ID)+'].png')
        
        plt.close(fig3)

        # ===========================================================================
        # Plot Histogram: Trips
        # =============================================================================
        trips_IDs = []
        # for n in range(min_ID,max_ID+1):
        #     if trips_by_ID[n] != 'no detections for this ID':
        #         for o in range(0,len(trips_by_ID[n])):
        #             trips_IDs.append(n)
        for ID in range(min_ID, max_ID+1):
            #print(ID)
            if trips_by_ID[ID] != 'no detections for this ID' and trips_by_ID[ID] != 'no clear trips for this ID' and trips_by_ID[ID] != 'only one detection for this ID':
                for trip in range(0,len(trips_by_ID[ID])):
                    trips_IDs.append(ID)
                    
        fig4 = plt.figure(4)
        plt.figure(figsize=(20, 12))
        
        counts_trip, edges_trip, bars_trip = plt.hist(trips_IDs, bins=(max_ID-min_ID+1), range=(min_ID,max_ID+1), color='#32ABE1')
        plt.grid(which='major',axis='y', linestyle='-')
        plt.bar_label(bars_trip, weight='bold')
        # set bin ticks and labels (uses same formatting as previous histogram)
        plt.xticks(ticks=range(min_ID,max_ID+1), labels=xtick_labels,fontsize=10)
        plt.yticks(fontsize=18)
        # plt.grid(b=True, which='major', axis='x', linestyle='-', color='#ededed')

        # set titles and axis labels
        plt.title('Frequency of Trips by ID', fontsize=30)
        # plt.title('From '+str(record_start_time)+' to '+str(record_end_time),fontsize=10)
        plt.xlabel('ID Number', fontsize=25)
        plt.ylabel('Frequency', fontsize=25)
        
        plt.savefig('../Results/' + colony + '_Trips_histograms_IDs['+str(min_ID)+','+str(max_ID)+'].png')

        plt.close(fig4)
        
        # ===========================================================================
        # Plot Histogram: Detections Events Trips
        # =============================================================================
        
        fig5 = plt.figure(5)
        plt.figure(figsize=(20, 12))
        
        counts_all, edges_all, bars_all = plt.hist([ID_num, event_IDs, trips_IDs], bins=(max_ID-min_ID+1), range=(min_ID,max_ID+1), histtype='bar', label = ['Detections', 'Events', 'Trips'])
        plt.grid(which='major',axis='y', linestyle='-')
        for b in bars_all:
            plt.bar_label(b, weight='bold')
        
        # set bin ticks and labels (uses same formatting as previous histogram)
        plt.xticks(ticks=range(min_ID,max_ID+1), labels=xtick_labels,fontsize=10)
        plt.yticks(fontsize=18)
        # plt.grid(b=True, which='major', axis='x', linestyle='-', color='#ededed')

        # set titles and axis labels
        plt.title('Detections - Events - Trips by ID', fontsize=30)
        # plt.title('From '+str(record_start_time)+' to '+str(record_end_time),fontsize=10)
        plt.xlabel('ID Number', fontsize=25)
        plt.ylabel('Frequency', fontsize=25)
        plt.legend(loc='upper left', ncols=3)
        
        plt.savefig('../Results/' + colony + '_All_histograms['+str(min_ID)+','+str(max_ID)+'].png')
        
        plt.close(fig5)
        
#%%        
    # =============================================================================
    # Plot trip length distribution for all IDs
    # =============================================================================
    all_trips_sec = []
    for ID in range(minID, maxID+1):
        if trips_by_ID[ID] != 'no detections for this ID' and trips_by_ID[ID] != 'no clear trips for this ID' and trips_by_ID[ID] != 'only one detection for this ID':
            for trip in range(0,len(trips_by_ID[ID])):
                all_trips_sec.append(trips_by_ID[ID][trip][3])
        
    # initialize plot
    #fig, ax = plt.subplots()
    fig20 = plt.figure(20)
    plt.figure(figsize=(20, 12))

    # set bin ticks and labels
    num_bins = 30
    time_ticks = [] # initialize ticks
    time_labels = [] # initialize tick labels
    # max_tick = max(all_trips_sec) + (500 - (max(all_trips_sec) % 500))
    max_tick = 7200 # 2 hours
    bin_width = int(max_tick / num_bins) # bins are 4 minutes long
    #bin_width = 120 # 2 minutes
    total_trips = len(all_trips_sec)
    # all trips less than max_thick
    all_trips_sec_less_than = [x for x in all_trips_sec if x <= max_tick]
    
    for n in range(0,max_tick+bin_width,bin_width):
        time_ticks.append(n)
        
        h = int( (n - n % 3600) / 3600 )
        t_left = n - h*3600
        m = int( (t_left - t_left % 60) / 60 )
        t_left = t_left - m*60
        s = int(t_left)
        
        minute_integer = int(n/60)
        
        if n % 240 == 0: # only show labels for every 4 minutes (to avoid crowding of labels)
            # time_labels.append(str(h)+':'+str(m)+':'+str(s))
            time_labels.append(str(minute_integer))
        else:
            time_labels.append('')
        
    counts, edges, bars = plt.hist(all_trips_sec_less_than, bins=num_bins, range=(0,7201), color='#ff9514')
    plt.grid(which='major',axis='y', linestyle='-')
    plt.grid(which='major',axis='x', linestyle='-', color = '#ededed')
    plt.bar_label(bars, weight='bold')
    # set bin ticks and labels
    plt.xticks(ticks=time_ticks, labels=time_labels, fontsize=14, rotation=0)
    plt.yticks(fontsize=18)
    total_trips_less_than = int(sum(counts))
    # set titles and axis labels
    plt.title('Distribution of Trip Lengths under 2 Hours ('+str(total_trips_less_than)+' out of '+str(total_trips)+' total)', fontsize = 30)
    plt.xlabel('Length (minutes)', fontsize = 30)
    plt.ylabel('Frequency', fontsize = 30)
    # Mean plot
    mean = stats.mean(all_trips_sec_less_than)
    mean_time = time.strftime("%M:%S", time.gmtime(mean))
    plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean*1.1, max_ylim*0.9, 'Mean: '+mean_time, weight='bold')
    
    # Median plot
    median = stats.median(all_trips_sec_less_than)
    median_time = time.strftime("%M:%S", time.gmtime(median))
    plt.axvline(median, color='k', linestyle='dashed', linewidth=1)
    plt.text(median*1.1, max_ylim*0.7, 'Median: ' + median_time, weight='bold')
    
    # Mode plot
    mode = stats.mode(all_trips_sec_less_than)
    mode_time = time.strftime("%M:%S", time.gmtime(mode))
    plt.axvline(mode, color='k', linestyle='dashed', linewidth=1)
    plt.text(mode*1.1, max_ylim*0.5, 'Mode: ' + mode_time, weight='bold')
    
    plt.savefig('../Results/' + colony + '_Trips_Length_IDs['+str(minID)+','+str(maxID)+'].png')
    
    plt.close(fig20)
        
        