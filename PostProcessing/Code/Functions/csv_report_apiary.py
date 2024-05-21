#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 18:20:23 2024

@author: diegop
"""


def csv_report_apiary(week, colony, p, start_datetime, stop_datetime, total_datetime, tagged_id):
    
    # create list of parameters, formatted as comma-separated strings and sorted by ID
    f_param_allRows = []
    f_param_allRows.append(' , , , , , , \n')
    
    f_param_titleRow = 'Apiary Statistics for 2xWeek "' + str(week) + '" \n' 
    f_param_allRows.append(f_param_titleRow)
    
    f_param_allRows.append(' , , , , , , \n')
    f_param_allRows.append(' , , , , , , \n')
    
    start_datetime.insert(0, 'Initial date (mm/dd/yy  hh:mm:ss)')
    f_param_allRows.append(str(start_datetime)[1:-1] + '\n')
    
    stop_datetime.insert(0, 'Final date (mm/dd/yy  hh:mm:ss)')
    f_param_allRows.append(str(stop_datetime)[1:-1] + '\n')
    
    total_datetime.insert(0, 'Total time (days hh:mm:ss)')
    f_param_allRows.append(str(total_datetime)[1:-1] + '\n')
    
    
    
    
    
    f_param_allRows.append(' , , , , , , \n')
    
    f_param_parametersRow = 'Parameters, Queen, Worker01, Worker02, Worker03, Worker04, Worker05\n'      
    f_param_allRows.append(f_param_parametersRow)
    
    
    f_param_allRows.append(' , , , , , , \n')
    
    
    p.tag_IDs_per_colony.insert(0, 'ID Tags Requested/Processed')
    f_param_allRows.append(str(p.tag_IDs_per_colony)[1:-1] + '\n')
    
    #### Here the excel file with the information about the IDs tagged should be displayed
    #f_param_allRows.append('IDs tagged in the field, ND, ND, ND, ND, ND, ND\n')
    tagged_id.insert(0, 'IDs tagged in the field')
    f_param_allRows.append(str(tagged_id)[1:-1] + '\n')
    
    f_param_allRows.append(' , , , , , , \n')
    
    
    # Add description to each parameter at the begining of the row, erase square brackets and append to csv file 
    p.percent_ID_detected = [round(e, 2) for e in p.percent_ID_detected]
    p.percent_ID_detected.insert(0, 'Percentage of ID detected (%) ')
    f_param_allRows.append(str(p.percent_ID_detected)[1:-1] + '\n')
    
    p.total_num_detections.insert(0, 'Total number of Detections ')
    f_param_allRows.append(str(p.total_num_detections)[1:-1] + '\n')
    
    p.total_num_events.insert(0, 'Total number of events ')
    f_param_allRows.append(str(p.total_num_events)[1:-1] + '\n')
    
    p.total_num_detections_per_event = [round(e, 2) for e in p.total_num_detections_per_event]
    p.total_num_detections_per_event.insert(0, 'Total average number of detections per event ')
    f_param_allRows.append(str(p.total_num_detections_per_event)[1:-1] + '\n')
    

    
    f_param_allRows.append(' , , , , , , \n')
    
    
    
    p.total_num_enter_events.insert(0, 'Total number of "enter" events ')
    f_param_allRows.append(str(p.total_num_enter_events)[1:-1] + '\n')
    
    p.total_percent_enter = [round(e, 2) for e in p.total_percent_enter]
    p.total_percent_enter.insert(0, 'Total percent of "enter" events (%) ')
    f_param_allRows.append(str(p.total_percent_enter)[1:-1] + '\n')
    
    p.total_num_exit_events.insert(0, 'Total number of "exit" events ')
    f_param_allRows.append(str(p.total_num_exit_events)[1:-1] + '\n')
    
    p.total_percent_exit = [round(e, 2) for e in p.total_percent_exit]
    p.total_percent_exit.insert(0, 'Total percent of "exit" events (%) ')
    f_param_allRows.append(str(p.total_percent_exit)[1:-1] + '\n')
    
    p.total_num_unknown_events.insert(0, 'Total number of "unknown" events ')
    f_param_allRows.append(str(p.total_num_unknown_events)[1:-1] + '\n')
    
    p.total_percent_unknow = [round(e, 2) for e in p.total_percent_unknow]
    p.total_percent_unknow.insert(0, 'Total percent of "unknown" events (%) ')
    f_param_allRows.append(str(p.total_percent_unknow)[1:-1] + '\n')
    
    p.total_avg_event_length_time.insert(0, 'Total Average Event Time (hh:mm:ss) ')
    f_param_allRows.append(str(p.total_avg_event_length_time)[1:-1] + '\n')
    
    p.total_avg_event_length_time_std.insert(0, 'Total Average Event Time Std Dev (hh:mm:ss) ')
    f_param_allRows.append(str(p.total_avg_event_length_time_std)[1:-1] + '\n')
    
    
    
    f_param_allRows.append(' , , , , , , \n')
    
    
    
    p.total_num_trips.insert(0, 'Total number of trips ')
    f_param_allRows.append(str(p.total_num_trips)[1:-1] + '\n')
    
    p.percent_events_for_trips = [round(e, 2) for e in p.percent_events_for_trips]
    p.percent_events_for_trips.insert(0, 'Total percentage of events used for Trips (%) ')
    f_param_allRows.append(str(p.percent_events_for_trips)[1:-1] + '\n')
    
    p.total_avg_trip_length_time.insert(0, 'Total Average Trip Time (hh:mm:ss) ')
    f_param_allRows.append(str(p.total_avg_trip_length_time)[1:-1] + '\n')
    
    p.total_avg_trip_length_stdev.insert(0, 'Total Average Trip Time Std Dev (hh:mm:ss)')
    f_param_allRows.append(str(p.total_avg_trip_length_stdev)[1:-1] + '\n')
    
    
    
    # write events to new file
    f_param = open('../Results/General_Report.csv', 'w') # $ change file name to avoid overwriting it, if necessary
    f_param.writelines(f_param_allRows)
    f_param.close()
    
    return
