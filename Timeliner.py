# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 18:47:52 2022

@author: yale-winter
yalewinter.com

- - - - - - - - - - - - - - - - - - - - - - - - -

TimeLiner - Make a simple timeline with MatPlotLib

- - - - - - - - - - - - - - - - - - - - - - - - -

Create a google sheet online or use with .csv offline 
The document needs the following schema:

Collumns: (A)Event  (B)Date   (C)Priority
Data:       Event 1    6.5.22      1
Data:       Event 2    6.14.22     3
etc ...

Plot Timelines with MatPlotLib

To load your live google sheet online:
Change import_online to True, and replace ___online_url___ with that part of your url

To load your offline .csv:
Download your Timeline as .csv (only downloading selected collumns and rows)
And name the document 'Timeline.csv' and place in the same folder

Run the script to plot your timelines
Priority >= 3 is for longest timeline
Priority >= 0 and < 3 is for recent timeline
Priority <= 0 is not displayed 
See the example .csv file (Timeline.csv) attached in this repository

"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates



def show_timeline(df, set_title):
    '''
    Display timelines
    '''
    df = df.sort_values(by=['Date'], ascending = False)
    #df = df[:len(df)]
    print(df)
    names = df[['Event']].to_numpy()
    dates = df[['Date']].to_numpy()
    # reshape to remove 1 dimension of array
    names = names.reshape(len(names),)

    ##############################################################################
    # Next, we'll create a stem plot with some variation in levels as to
    # distinguish even close-by events. We add markers on the baseline for visual
    # emphasis on the one-dimensional nature of the time line.
    #
    # For each event, we add a text label via `~.Axes.annotate`, which is offset
    # in units of points from the tip of the event line.
    #
    # Note that Matplotlib will automatically plot datetime inputs.
    
    
    # Choose some nice levels
    levels = np.tile([-9,9,-7,7,-5, 5, -3, 3, -1, 1],
                     int(np.ceil(len(dates)/10)))[:len(dates)]
    
    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title=set_title)
    
    ax.vlines(dates, 0, levels, color="tab:blue")  # The vertical stems.
    ax.plot(dates, np.zeros_like(dates), "-o",
            color="k", markerfacecolor="w")  # Baseline and markers on it.
    
    # annotate lines
    for d, l, r in zip(dates, levels, names):
        ax.annotate(r, xy=(d, l),
                    xytext=(-3, np.sign(l)*3), textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="bottom" if l > 0 else "top")
    
    # format xaxis with 4 month intervals
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    
    # remove y axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)
    
    ax.margins(y=0.1)
    

    plt.show()


def import_timeline(file_name, online, read_rows):
    '''
    Import timeline from .csv file
    '''
    df = []
    try:
        if online:
            df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                               '___online_url___' +
                               '/export?gid=0&format=csv',
                              )
        else:
            # file path (same directory as this file)
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            sheet_url = os.path.join(__location__, file_name)
            df = pd.read_csv(sheet_url, nrows=read_rows, on_bad_lines='skip')
            
        df.dropna(how='all')
        ldf = df.values.tolist()
        #convert datetime
        for i in range(len(ldf)):
            ldf[i][1] = pd.to_datetime(df.iloc[i][1])
        df = pd.DataFrame(ldf, columns=['Event', 'Date', 'Priority'])
    except:
        print('problem importing data')
    return df

'''
Start up and display Timelines
'''
import_online = False
set_title = "Timeline"
df = import_timeline('Timeline.csv', import_online, 1000)
#print(df)
show_timeline(df, set_title)