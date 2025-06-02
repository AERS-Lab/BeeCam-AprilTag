#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:31:18 2024

@author: diegop
"""
import numpy as np

def enter_or_exit_vector(angles,threshold):
    '''This function assigns "exit" or "enter" to an event based on the summed 
    vector direction/angle. It requires the ANGLES (measured counterclockwise
    from the positive x-axis) of each detection within the event. It also
    requires the desired THRESHOLD angle (in degrees), i.e. the minimum angle
    away from the x-axis in any direction that must be reached by the summed
    vector direction to reasonably estimate "enter" or "exit". 
    
    For example, if the given threshold angle is 30 degrees, [30, 150] is the
    range in which the event will be labeled an "enter." [210,330] is an
    "exit", and anything outside both of those ranges is an "unknown".
    
    The function usually returns a list with the event type ("enter", "exit", or
    "unknown"), the given threshold angle (in degrees), and the summed vector 
    angle (in degrees). However, if the vector direction sums to zero, an 
    error string is returned.'''
    
    # determine change in x and y for each detection
    # each detection is weighted equally (vector magnitude = 1)
    dx = np.cos(np.deg2rad(angles)) 
    dy = np.sin(np.deg2rad(angles))
    
    # add individual detection vector directions
    # divide by number of detections so that summed vector is normalized to a magnitude of 1, as only the vector direction matters
    vector_x = sum(dx) / len(dx)
    vector_y = sum(dy) / len(dy)
    
    if vector_x == 0 and vector_y == 0:
        # if the bee faced each direction an equal amount, return an error
        return 'zero vector error'
    elif vector_x == 0 and vector_y != 0:
        # manually assign angles when x = 0 to avoid division by zero error
        if vector_y > 0:
            deg = 270
        elif vector_y < 0:
            deg = 90
    else:
        # determine direction angle using arctan
        deg = np.rad2deg(np.arctan(vector_y/vector_x))
        
        # since arctan limits are (-90,90), use coordinate directions to 
        # correct the angle to be within standard [0,360) range
        if vector_x > 0 and vector_y >= 0:
            deg = deg
        elif vector_x < 0 and vector_y >= 0:
            deg = 180 + deg
        elif vector_x < 0 and vector_y < 0:
            deg = deg + 180
        elif vector_x > 0 and vector_y < 0:
            deg = 360 + deg
    
    # set exit and enter ranges using given threshold
    # measured counterclockwise from positive x
    exit_min = 180 + threshold
    exit_max = 360 - threshold
    enter_min = threshold
    enter_max = 180 - threshold
    
    if deg >= exit_min and deg <= exit_max:
        # if summed vector angle is within the exit range of angles
        return ['exit',threshold,deg]
    elif deg >= enter_min and deg <= enter_max:
        # if summed vector angle is within the enter range of angles
        return ['enter',threshold,deg]
    else:
        # if summed vector angle is not within exit or enter ranges of angles
        return  ['unknown',threshold,deg]
    