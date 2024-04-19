#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:08:52 2024

@author: diegop
"""

# ===========================================================================
# Generate a csv file with info for all detections and all identified events
# (files generated in same directory as this .py file)
# =============================================================================


def csv_events(colony, events_by_ID):
    
    # create list of events, formatted as comma-separated strings and sorted by ID
    f_events_allRows = []
    f_events_titleRow = 'ID_num,num_of_detections,original_index_start,start_time,original_index_end,end_time,event_type_by_y_location,event_type_by_summed_vector_direction,event_type_by_x_location,event_result,summed_vector_angle_degrees, ,detections_index\n'      
    f_events_allRows.append(f_events_titleRow)
    for u in range(0,len(events_by_ID)):
        if events_by_ID[u] != 'no detections for this ID':
            for v in range(0,len(events_by_ID[u])):
                if len(events_by_ID[u][v]) == 8: # there was an error with some mis-detected IDs not recording all info; filter these out
                    next_row = str(u)
                    next_row+= ',' + str(events_by_ID[u][v][2] - events_by_ID[u][v][0] + 1)
                    next_row+= ',' + str(events_by_ID[u][v][0])
                    next_row+= ',' + str(events_by_ID[u][v][1])
                    next_row+= ',' + str(events_by_ID[u][v][2])
                    next_row+= ',' + str(events_by_ID[u][v][3])
                    next_row+= ',' + events_by_ID[u][v][4]
                    next_row+= ',' + events_by_ID[u][v][5][0]
                    next_row+= ',' + events_by_ID[u][v][6]
                    if events_by_ID[u][v][4] == 'enter' and events_by_ID[u][v][5][0] == 'enter' and events_by_ID[u][v][6] == 'right_enter':
                        next_row+= ',' + 'ENTER'
                    elif events_by_ID[u][v][4] == 'enter' and events_by_ID[u][v][5][0] == 'enter' and events_by_ID[u][v][6] == 'left_exit':
                        next_row+= ',' + 'ENTER_Wrong_Tunnel!'
                    elif events_by_ID[u][v][4] == 'exit' and events_by_ID[u][v][5][0] == 'exit' and events_by_ID[u][v][6] == 'left_exit':
                        next_row+= ',' + 'EXIT'
                    elif events_by_ID[u][v][4] == 'exit' and events_by_ID[u][v][5][0] == 'exit' and events_by_ID[u][v][6] == 'right_enter':
                        next_row+= ',' + 'EXIT_Wrong_Tunnel!'    
                    else:
                        next_row+= ',' + 'UNKNOWN'
                    #next_row+= ',' + str(events_by_ID[u][v][5][1])
                    next_row+= ',' + str(events_by_ID[u][v][5][2])
                    
                    list_index = str(events_by_ID[u][v][7]).replace('[','')
                    list_index = list_index.replace(']','')
                    
                    next_row+= ',' + ''
                    next_row+= ',' + list_index  + '\n'
                    f_events_allRows.append(next_row)
    
    # write events to new file
    f_events = open('../Results/' + colony + '_Events_by_ID_v1.csv', 'w') # $ change file name to avoid overwriting it, if necessary
    f_events.writelines(f_events_allRows)
    f_events.close()
        
    return