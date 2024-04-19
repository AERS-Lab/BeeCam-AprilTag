#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:00:32 2024

@author: diegop
"""

def enter_or_exit_x(x_start,x_end):   
    '''This function assigns "right_exit", "left_enter", or "Uknown"
    to an event based on the starting/ending x-coordinates in an
    event. It requires the x-coordinate of the first detection 
    (x_start) and the x-coordinate of the last detection (x-end).
    '''    
    if x_start < 366 and x_end < 366:
        return 'right_enter'
    elif x_start > 366 and x_end > 366:
        return 'left_exit'
    else:
        return 'unknown'