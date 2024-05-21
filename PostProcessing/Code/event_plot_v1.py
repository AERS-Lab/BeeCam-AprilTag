#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 15:06:39 2024

@author: diegop
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import csv

def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]
    Code from Brendan Artley via Medium
    https://medium.com/@BrendanArtley/matplotlib-color-gradients-21374910584b"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    Code from Brendan Artley via Medium
    https://medium.com/@BrendanArtley/matplotlib-color-gradients-21374910584b
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]
        

# =============================================================================
# Load data
# =============================================================================

# read .txt file
with open('../Data/worker05.txt') as file: # $ change file name if necessary
    lines = file.readlines()
    file.close()

# initialize lists
center_x = []
center_y = []
angle = []
time = []
ID_num = []
date = []

### Select event using Excel-file "events_by_ID_v1.csv" index 

index = input("Select the index: ")

with open('../Results/worker05_Events_by_ID_v1.csv') as file: # $ change file name if necessary
    rows = csv.reader(file)
    events_list = list(rows)
    file.close()

lis = events_list[int(index)-1][11:len(events_list[int(index)-1])]
list_of_index = [int(i) for i in lis]
#lower_idx = int(events_list[int(index)-1][2]) # $ index of the first detection that will be plotted
              # you can manually choose it from the original data file (line # + 1)
              # OR you can choose it from one of the events in the 2nd .csv file output by detections_analysis.py (original_index_start)
#upper_idx = int(events_list[int(index)-1][4]) # $ index of the first detection that will be plotted
              # you can manually choose it from the original data file (line # + 1)
              # OR you can choose it from one of the events in the 2nd .csv file output by detections_analysis.py (original_index_end)
              
for i in list_of_index:
    # replace unnecessary characters in line
    line = lines[i]
    line = line.replace('[','')
    line = line.replace(']','')
    line = line.replace('CPU','')
        
    # split line by spaces
    line = line.split()
    
    # extract info and convert to usable types
    center_x.append(float(line[8]))
    center_y.append(float(line[9]))
    angle.append(float(line[11]))
    time.append(line[3])
    ID_num.append(int(line[6]))
    date.append(line[1] +' '+ line[2] +' '+  line[4])

# =============================================================================
# Create vectors/arrows for plotting
# =============================================================================
    
arrow_len = 10 # arrow length

# define arrow starting points with start of arrow = (center_x,center_y)
arrow_x = center_x
arrow_y = center_y

# define arrow ending point
dx = arrow_len*np.cos(np.deg2rad(angle))
dy = -arrow_len*np.sin(np.deg2rad(angle))


# =============================================================================
# Create plot
# =============================================================================

# initialize plot
fig, ax = plt.subplots(figsize=(13.5,10))

# sum vector directions
sum_vector_x = sum(dx) / len(dx) * arrow_len
sum_vector_y = sum(dy) / len(dx) * arrow_len

# show the tick labels on top
ax.xaxis.set_tick_params(top=True, labeltop=True)

# hide the tick labels on bottom
ax.xaxis.set_tick_params(bottom=False, labelbottom=False)

num = 1 # initialize arrow order

if len(arrow_x)==1:
    colors = get_color_gradient('#ffffff','#f58700',2)
else:
    colors = get_color_gradient('#ffffff','#f58700',len(arrow_x))
        

#colors = get_color_gradient('#ffffff','#f58700',len(arrow_x))
#colors = get_color_gradient('#ffffff','#f58700',2)

for k in range(0,len(arrow_x)):
    
    # plot each arrow
    plt.arrow(arrow_x[k], arrow_y[k], dx[k], dy[k], width=1.5, head_width=8, fc=colors[k], ec='k')
    
    # label first and last arrow with order and time 
    if num==1:
        plt.annotate('Start\n' + time[k], ha='center', xy = (arrow_x[k], arrow_y[k]-2), size=20, weight='bold')
    elif num==len(arrow_x): 
        plt.annotate('End\n' + time[k], ha='center', xy = (arrow_x[k], arrow_y[k]-2), size=20, weight='bold')
        
    # else: # label all other arrows only with order
        # plt.annotate(num, xy = (arrow_x[k], arrow_y[k]), size=10)
        
    num += 1 # add 1 to order for next arrow

# show summed vector direction (location of arrow is not significant)
plot_center_x = 363
plot_center_y = 160
plt.arrow(plot_center_x, plot_center_y, sum_vector_x, sum_vector_y, width=2, head_width=10, fc='#150fd1', ec='#150fd1')
plt.annotate('Summed\nVector\nDirection', ha='center',xy = (plot_center_x, plot_center_y-5), size=20, weight='bold',color='#150fd1')


# set titles and axis labels
plt.xlabel('x-axis pixels',fontsize=15)
ax.xaxis.set_label_position('top') 
plt.ylabel('y-axis pixels',fontsize=15)
if sum(ID_num) / len(ID_num) == ID_num[0]:
    plt.title('Bee Detection (ID = '+str(ID_num[0])+') (Index = '+ str(index)+') Start: '+ str(date[0])+' | End: '+str(date[-1]) +'\n'+'L_method: '+events_list[int(index)-1][6]+'  V_method: '+events_list[int(index)-1][7]+'  Result: '+events_list[int(index)-1][8], fontsize = 15, weight='bold')
else:
    plt.title('Bee Detection Locations and Directions (multiple IDs)',fontsize=30)


# set x and y axis limits
plt.xlim([0, 800])
plt.ylim([0, 320])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid()

plt.plot(center_x, center_y, 'x--', lw=2, color='black', ms=10)

# invert axis to be consistent with camera preview
ax.invert_yaxis() 

# label hive and entrance sides
plt.annotate('Hive', xy=(375,15), color ='#150fd1', weight='bold',fontsize=20)
plt.annotate('Entrance', xy=(350,320-5), color ='#150fd1', weight='bold',fontsize=20)

#plt.annotate('Wire In', xy=(100,15), color ='#150fd1', weight='bold',fontsize=20)
#plt.annotate('Wire Out', xy=(520,320-5), color ='#150fd1', weight='bold',fontsize=20)


plt.show()
