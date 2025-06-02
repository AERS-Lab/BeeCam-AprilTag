#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:43:50 2024

@author: diegop
"""


def enter_or_exit_y(y_start,y_end):
    '''This function assigns "exit", "enter", "failed_to_enter," or 
    "failed_to_exit" to an event based on the starting and ending y-coordinates
    of the event. It requires the y-coordinate of the first detection 
    (y_start) and the y-coordinate of the last detection (y-end).
    
    The y-coordinate is 0 at the hive and increases towards the entrance (i.e. 
    the positive y-axis points down on a plot). Therefore, if y_start is
    GREATER than y_end by a certain amount, the function returns 'enter' for 
    that event. If y_start is LESS than y_end by a certain amount, the
    functions returns 'exit' for that event.
    
    Else, if the difference between y_start and y_end is not greater in
    magnitude than the certain amount, but y_start and y_end are each GREATER
    than a certain y-coordinate (i.e. both are near the entrance), the function
    returns 'failed_to_enter' (the bee entered but immediately re-exited).
    Similarly, if the difference between y_start and y_end is not greater in
    magnitude than the certain amount, but y_start and y_end are each LESS
    than a certain y-coordinate (i.e. both are near the hive), the function 
    returns 'failed_to_enter' (the bee exited the hive but immediately 
    re-entered).
    
    If none of these conditions are met, the functions returns 'unknown'.'''
    
    if y_start - y_end > 10: # set the 'enter' threshold
        return 'enter'
    elif y_start - y_end < -10: # set the 'exit' threshold (number must stay negative)
        return 'exit'
    #elif y_start > 250 and y_end > 250: # set the 'failed_to_enter' threshold
    #    return 'failed_to_enter'
    #elif y_start < 50 and y_end < 50: # set the 'failed_to_exit' threshold
    #    return 'failed_to_exit'
    else: # if event type can't be determined within the desired thresholds
        return 'unknown'
    