#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:22:31 2024

@author: diegop
"""

from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
  
# plot function is created for  
# plotting the graph in  
# tkinter window 
def plot(): 
    value = spinbox.get()
    p = eval(value)
    print('value change to: ', type(p))
    
    # the figure that will contain the plot 
    fig = Figure(figsize = (5, 5), dpi = 100) 
  
    # list of squares 
    y = [p*i**2 for i in range(101)] 
    print(y)
    # adding the subplot 
    plot1 = fig.add_subplot(111) 
    plot1.clear()
    # plotting the graph 
    plot1.plot(y) 
  
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, 
                               master = window)   
    canvas.draw() 
    
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
    
    
  
    # # creating the Matplotlib toolbar 
    # toolbar = NavigationToolbar2Tk(canvas, 
    #                                window) 
    # toolbar.update() 
  
    # # placing the toolbar on the Tkinter window 
    # canvas.get_tk_widget().pack()
    
    
    
    
    
# the main Tkinter window 
window = Tk() 
  
# setting the title  
window.title('Plotting in Tkinter') 
  
# dimensions of the main window 
window.geometry("500x500") 
  
# Creating a Spinbox
spinbox = Spinbox(window, from_=0, to=100, width=10, relief="sunken", repeatdelay=500, repeatinterval=100,
                     font=("Arial", 12), bg="lightgrey", fg="blue", command=plot )
spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)

# Placing the Spinbox in the window
spinbox.pack(padx=20, pady=20)

# run the gui 
window.mainloop() 