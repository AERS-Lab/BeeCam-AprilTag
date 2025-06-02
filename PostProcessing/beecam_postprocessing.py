# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:28:42 2024

@author: sarab
"""

import pandas as pd
import datetime as dt
import numpy as np

"""
This file contains all post-processing and data manipulation functions for the data text files 
retrieved from a BeeCam system.

"""
#=============================================================================
# "text2df" converts one detections text file into a pandas DataFrame
# Parameters:
    # textFile: path to text file
    # keep_corr_lines: False by default. If True, return list of corrupted lines
# Returns:
    # data: DataFrame where each row is a detection
    # corr_lines: list of corrupted text lines 
#=============================================================================
def text2df(textFile, keep_corr_lines=False):
    #First, clean text for data frame conversion
    with open(textFile) as file:
        #read text file into list
        lines = file.readlines()
        file.close()
    
    corr_lines=[]
    for line in range(0,len(lines)):
        # remove unnecessary characters in line
        lines[line] = lines[line].replace('[ ', '')
        lines[line] = lines[line].replace('[','')
        lines[line] = lines[line].replace(']','')
        lines[line] = lines[line].replace('CPU','')
          
        # split line by spaces to create list of terms
        lines[line] = lines[line].split()
        # remove day of week
        del lines[line][0]
        if len(lines[line]) != 13:
            print("Line " + str(line) + " is corrupted. Removing from dataframe.")
            corr_lines.append(line)
        # remove text file data labels from term list
        text_file_labels = [term for term in lines[line] if term.endswith(':')]
        lines[line] = [el for el in lines[line] if el not in text_file_labels]
    
    #remove corrupted lines
    lines = [lines[line] for line in range(0,len(lines)) if line not in corr_lines]
    #create DataFrame from lines
    data = pd.DataFrame(lines)
    
    #create column labels
    labels = ['month', 'day', 'time', 'year', 'ID', 'center_x', 'center_y', 'angle', 'CPUtemp']
    data.columns = labels

    #data types for each column
    dtype_dict = {'month': str,
                  'day': str,
                  'time': str,
                  'year': str,
                  'ID': int, 
                  'center_x': float,
                  'center_y': float,
                  'angle': float,
                  'CPUtemp': float 
                  }

    #convert data to appropriate dtypes
    data['month']=data['month'].str.zfill(2)
    data['day']=data['day'].str.zfill(2)
    data = data.astype(dtype_dict)
    
    #round floats to two decimals
    data = data.round(2)

    #convert date to datetime format in new column
    data['DT'] = data[['month','day','year']].agg('-'.join, axis=1)
    data['DT'] = data['DT'] + ' ' + data['time']
    data['DT'] = data['DT'].apply(pd.to_datetime, format='%b-%d-%Y %H:%M:%S')
    
    #remove redundant date/time string columns
    data = data.drop(['month', 'day', 'year', 'time'], axis=1)
    
    if keep_corr_lines:
        return data, corr_lines
    else:
        return data
#=============================================================================
# "get_tagging_log" converts a tagging log csv file into a DataFrame
# Parameters:
    # tagging_log_path: path to csv file where tagging sessions were recorded
# Returns:
    # tagging_log: DataFrame containing all tagging sessions
#=============================================================================
def get_tagging_log(tagging_log_path):
    #get tagging log as dataframe from the main Excel file
    tagging_log = pd.read_csv(tagging_log_path)
    tagging_log['Date'] = pd.to_datetime(tagging_log['Date'])
    
    def is_int(log_row):
        try:
            log_row[["Tags start", "Tags end"]] = log_row[["Tags start", "Tags end"]].astype(int)
        except ValueError:
            return False
        else:
            return True
    
    tagging_log = tagging_log[tagging_log.apply(is_int, axis=1)]
    tagging_log['Date'] = pd.to_datetime(tagging_log['Date'])
    
    return tagging_log


# The next functions assume the log contains records for only one location
# or apiary.
# If the log contains multiple apiaries, you want to filter it
# for only one location of interest with
# apiary_log = tagging_log[[tagging_log['Location']=="Name_of_Location"]]
# This will filter out ID numbers that appear in one apiary, but not another
# One colony may see detections from a neighbor colony's bees, which is normal.

#=============================================================================
# "filter_data" removes all detections that contain either unlogged ID numbers
# or dates before the first tagging date.
# Parameters:
    # data: DataFrame of detections
    # tagging_log: DataFrame of tagging sessions
    # keep_omitted_det: False by default. If True, function returns separate
    # DataFrame of detections that were filtered out
# Returns:
    # detections: Filtered detections DataFrame
    # omitted_detections: DataFrame of faulty detections
#=============================================================================
def filter_data(data, tagging_log, keep_omitted_det=False):
    # Remove detections with dates prior to first tagging session
    start_date = tagging_log['Date'].min()
    detections = data[(data['DT'].dt.date >= start_date.date())]
    
    # Remove detections of unlogged IDs:
    # 1. Create array of all logged tag ranges
    tag_full_range = lambda x: np.arange(int(x['Tags start']), int(x['Tags end'])+1,1)
    logged_IDs = tagging_log[['Tags start','Tags end']].apply(tag_full_range, axis=1).to_numpy()
    
    # 2. Create boolean mask to filter unlogged IDs from detections
    logged_ID_detections = detections['ID'].apply((lambda x: any(x in a for a in logged_IDs)))
    
    detections = detections[logged_ID_detections]
    omitted_detections = data[(~logged_ID_detections) | ((data['DT'].dt.date < start_date.date()))]
    
    if keep_omitted_det:
        return detections, omitted_detections
    else:
        return detections

#=============================================================================
# "enter_or_exit" is used to calculate the vector angle sum of all detections
# in an event to classify it as "enter", "exit", or "unknown"
# Parameters:
    # angles: List of detection angles in an event
    # threshold: angle threshold (in degrees) used to assign event types
# Returns:
    # [event_type, deg]: List containing the event type and vector angle sum
#=============================================================================
def enter_or_exit(angles, threshold):
    dx = np.cos(np.deg2rad(angles)) 
    dy = np.sin(np.deg2rad(angles))
        
    # add individual detection vector directions
    # divide by number of detections so that summed vector is normalized to a magnitude of 1, as only the vector direction matters
    vector_x = sum(dx) / len(dx)
    vector_y = sum(dy) / len(dy)
    
    # Calculate the vector sum angle with arctan
    try:
        deg = np.rad2deg(np.arctan(vector_y/vector_x))
   
    except ZeroDivisionError:
        # Handle cases where vector_x = 0
        if vector_y == 0:
            deg = 0
        elif vector_y < 0:
            deg = 90
        elif vector_y > 0:
            deg = 270
            
    else:
        # since arctan limits are (-90,90), use coordinate directions to 
        # correct the angle to be within standard [0,360) range
        if vector_x < 0:
            deg = 180 + deg
        elif vector_y < 0:
            deg = 360 + deg
    
    # set exit and enter ranges using input threshold
    exit_min = 270 - threshold
    exit_max = 270 + threshold
    enter_min = 90 - threshold
    enter_max = 90 + threshold
        
    if deg >= exit_min and deg <= exit_max:
        # if summed vector angle is within the exit range of angles
        return ['exit',deg]
    elif deg >= enter_min and deg <= enter_max:
        # if summed vector angle is within the enter range of angles
        return ['enter',deg]
    else:
        # if summed vector angle is not within exit or enter ranges of angles
        return ['unknown',deg]

#=============================================================================
# "get_events" sorts detections into events based on a minimum duration
# between events. Then, each event is classified as "exit", "enter", or "unknown"

# Parameters:
    # data: DataFrame of detections
    # minimum_time_delta: Minimum duration (in seconds) between events
    # default is 60 seconds
    # angle_threshold: angle threshold (in degrees) used to assign event types
    # default is 60 degrees
# Returns:
    # events: 3-level (ID, event, detection) multi-indexed DataFrame 
#=============================================================================
def get_events(data, minimum_time_delta=60, angle_threshold=60):
    #Sort data by ID number, then by detection time
    data_by_ID = data.sort_values(['ID', 'DT'])
    data_by_ID.index = data_by_ID.index.set_names("detection")
    
    # The groupby function splits the DataFrame into groups so that we can apply
    # a function to each group separately.
    #Group the data by ID number
    data_grouped = data_by_ID.groupby('ID')
    
    # Calculate the difference in time between each detection and the 
    # previous detection for each ID.
    time_delta = data_grouped['DT'].diff().dt.total_seconds()
    
    # Insert the time_delta into DataFrame
    data_by_ID.insert(1,'time_delta', time_delta)
    
    # Identify events for each ID based on time_delta. If the time_delta is
    # greater than the minimum, start new event by incrementing event counter.
    data_grouped = data_by_ID.groupby(['ID'])
    event_number = data_grouped['time_delta'].apply(lambda x: (x > minimum_time_delta).cumsum())
    data_by_ID.insert(1,'event', event_number.droplevel(0))
    
    # Group data by ID and event number.
    events_grouped = data_by_ID.groupby(['ID','event'])
    
    # Classify each event and get event duration (if more than one detection per event)
    event_type = events_grouped['angle'].apply(enter_or_exit, threshold=(angle_threshold))
    #event_duration = events_grouped.agg({'time_delta': 'sum'}) - events_grouped.agg({'time_delta': 'first'})

    
    #Create multilevel-indexed DataFrame.
    #First level is ID
    #Second is event number
    #Third is detection number
    events = pd.pivot_table(data_by_ID, index = ['ID', 'event','detection'])
    
    #Insert colums for event type and angle sum 
    events.insert(0,'type', event_type.apply(lambda x: x[0]))
    events.insert(0,'sum_angle', event_type.apply(lambda x: x[1]))
    
    return events

#=============================================================================
# "get_trips" extracts trips from all events by identifying consecutive 
# "exit" and "enter" events for each ID

# Parameters:
    # events: DataFrame of events
    # max_trip_duration: Maximum trip duration (Timedelta object)
    # default is 2 hours
# Returns:
    # trips: 4-level (ID, trip, event, detection) multi-indexed DataFrame 
#=============================================================================
def get_trips(events, max_trip_duration=dt.timedelta(hours=2)):
    # Identify consecutive "exit" and "enter" events    
    
    # 1. Group events by ID
    events_by_ID = events.groupby(['ID'])
    # 2. Get previous event type by shifting event type down one row
    prev_events = events_by_ID['type'].shift(1)
    # 3. Drop detection detection level so each event is one row
    prev_events = prev_events.groupby(['ID','event']).nth(0).droplevel('detection')
    # 4. Get current events
    curr_events = events.groupby(['ID','event'])['type'].nth(0).droplevel('detection')
    
    # 5. Create boolean mask to find which events make up a trip.
    # Find enter events where the prev event was an "exit"
    trip_enter = curr_events.where((curr_events=='enter') & (prev_events=='exit')).notna()
    trip_exit = trip_enter.shift(-1)
    # Or operation so all events in a trip are True
    is_trip = trip_exit | trip_enter
   
    # 6. Assign trip number to all event pairs
    trip_events = events[is_trip]
    trip_number = trip_exit.eq(True).cumsum()
    trip_events.insert(1,'trip', trip_number)

    # Create multiindexed dataframe with events organized into trips for each ID
    trips = pd.pivot_table(trip_events, index = ['ID','trip','event','detection'], aggfunc=(lambda x: x))
    
    # Get trip durations from enter and exit times

    try:
        # For each trip, subtract the min detection DT from the max detection DT 
        # Create boolean mask to separate trip events
        trip_exits = trips['type'].isin(['exit'])
        trip_enters = trips['type'].isin(['enter'])
        
        # Trip begins at latest exit DT and ends at earliest enter DT
        trips['DT_Enter'] = trips[trip_enters]['DT'].groupby(['ID','trip']).min()
        trips['DT_Exit'] = trips[trip_exits]['DT'].groupby(['ID','trip']).max()
        trips['Duration'] = trips['DT_Enter'] - trips['DT_Exit']
        
        # Sort for easier reading
        trips = trips.sort_values(['ID', 'DT'])
        
        # Drop trips that are longer than max duration
        trips = trips[trips['Duration'] < max_trip_duration]
   
   # Resolve error if no trips found 
    except KeyError as error:
        print('No trips found for this worker: ', error)
        
    return trips

#=============================================================================
# "trips_csv" generates a summary csv file of all trips found

# Parameters:
    # filename: where the csv will be written to
    # trips_data: 4-level (ID, trip, event, detection) trips DataFrame 
    # apiary_log: tagging log DataFrame for the apiary

# Returns:
    # new csv file where every row is a trip with columns cotaining:
    # colony where trip was detected, ID, exit datetime, enter datetime, 
    # duration, days since tag was first placed, and ID colony of origin
#=============================================================================
def trips_csv(filename, trips_data, apiary_log):
    
    #Create separate log for repeat ID numbers (Aug 20th and onwards)
    repeat_date = dt.datetime(2024, 8, 20)
    repeat_log = apiary_log[apiary_log['Date']>=repeat_date]
    
    tag_full_range = lambda x: np.arange(int(x['Tags start']), int(x['Tags end'])+1,1)
    repeat_IDs = repeat_log[['Tags start','Tags end']].apply(tag_full_range, axis=1).to_numpy()
    repeat_IDs = np.concatenate(repeat_IDs)
    
    # We only want trip info, so we remove event and detection metadata
    # 1. Reset index to 1D
    trips = trips_data.reset_index()
    
    # 2. Remove event and detection info
    trips = trips.drop(['event','detection','CPUtemp','DT', 'angle', 'center_x', 'center_y', 'sum_angle','time_delta','type'], axis=1)
    
    # 3. Remove duplicate rows, leaving one row per trip
    trips = trips.drop_duplicates()
    # Get tagging dates and match detected IDs to colony of origin
    #functions to find tag info in apiary log
    #tag_date_finder = lambda row: apiary_log[(row['ID'] >= apiary_log['Tags start']) & (row['ID'] <= apiary_log['Tags end'].astype(int))]['Date'].iloc[0]
    #repeat_date_finder = lambda ID: repeat_log[(ID >= repeat_log['Tags start']) & (ID <= repeat_log['Tags end'].astype(int))]['Date'].iloc[0:0]
    
    tag_colony_finder = lambda ID: apiary_log[(ID >= apiary_log['Tags start']) & (ID <= apiary_log['Tags end'])]['Pi ID'].iloc[0]
    
    def tag_date_finder(row):
        if row['Repeat_ID']:
            return repeat_log[(row['ID'] >= repeat_log['Tags start']) & (row['ID'] <= (repeat_log['Tags start'].astype(int) + 99))]['Date'].iloc[0]
        else:
            return apiary_log[(row['ID'] >= apiary_log['Tags start']) & (row['ID'] <= (apiary_log['Tags start'].astype(int) + 99))]['Date'].iloc[0]
   
    #add tag date to each trip
    is_repeat = lambda row: (row['DT_Exit']>=repeat_date) & (row['ID'] in repeat_IDs)
    trips['Repeat_ID'] = trips.apply(is_repeat, axis=1)
    
    trips['Tag_Date'] = trips[['ID','Repeat_ID']].apply(tag_date_finder, axis=1)
    
    #add the number of days (rounded to the nearest day) since tag first applied
    trips['Days_Since_Tag_Date'] = (pd.to_datetime(trips['DT_Exit']) - pd.to_datetime(trips['Tag_Date'])).dt.round('d')
    
    #add colony that the tagged bee originates from
    trips['Tag_Colony_Origin'] = trips['ID'].apply(tag_colony_finder)
    
    #Format function for trip durations
    def format_td(total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    
    #apply format to trip durations
    trips['Duration'] = trips['Duration'].dt.total_seconds().apply(format_td)    
    
    #Save final dataframe to csv file
    trips.to_csv(filename, index=False)
    
#=============================================================================
# "count_groups" counts groups in events or trips DataFrame. 
# Gives number of unique colonies, IDs trips, events, or detections

# Parameters:
    # DF: DataFrame or dictionary of multiple DataFrames
    # group: string of which group to count. Can be one of the following:
    # 'colony', 'ID', 'trip', 'event', or 'detection'

# Returns:
    # count: number of the specified group in the input DataFrame
#=============================================================================
def count_groups(DF, group):
    # Check if dictionary of dataframes
    group_names = ['colony', 'ID', 'trip', 'event', 'detection']
    if isinstance(DF, dict):
        trips = pd.concat(DF, names=group_names)
    else:
        trips = DF

    group_to_count = group_names[:group_names.index(group)+1]
    
    count = trips.groupby(group_to_count).ngroups
    return count

