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

To load your live google sheet online (set so anyone with the link can view):
Change import_online to True, and replace your_url_here with that part of your url

To load your offline .csv:
Download your table as .csv (only downloading selected collumns and rows)
And name the document 'Timeline.csv' and place in the same folder

How to Use:
Run the script to plot your timelines
Priority <= 0 is not displayed 
See the example .csv file (Timeline.csv) attached in this repository

"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates


def show_timeline(df, set_title, max_events):
    '''
    Display timeline with DataFrame, Title, Max Events
    '''
    # if didn't get DataFrame then return
    if type(df) != pd.DataFrame:
        return
    
    #sort
    df = df.sort_values(by=['Date'], ascending = False)
    
    # limit to max events
    if max_events < len(df):
        df = df[:len(df)]
    
    # remove low priority
    df = df.loc[df['Priority'] > 0,:]
    
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
    fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
    ax.set(title=set_title)
    
    ax.vlines(dates, 0, levels, color="tab:orange")  # The vertical stems.
    ax.plot(dates, np.zeros_like(dates), "-o",
            color="tab:blue", markerfacecolor="w")  # Baseline and markers on it.
    
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


def fix_dates_in_col(df, col_index, col_names):
    '''
    Formats dates in a collumn
    ----------
    Returns
    -------
    modified DataFrame

    '''
    ldf = df.values.tolist()
    for i in range(len(ldf)):
        ldf[i][col_index] = pd.to_datetime(df.iloc[i][col_index])
    df = pd.DataFrame(ldf, columns=col_names)  
    return df

def import_data_table(file_name, read_rows, col_names):
    '''
    Import timeline from .csv file
    
    Parameters
    ----------
    file_name : string
        File name including file extension
    read_rows : number
        number of rows to read
    col_names : array of strings
        names of columns

    Returns
    -------
    DataFrame of the content or error string

    '''
    df = 'error importing data'
    try:
        df = pd.read_csv(file_name,nrows=read_rows, on_bad_lines='skip')
        print('loaded data table from local .csv')
    except:
        print('error loading data from local .csv')

    # drop rows where at least 1 element is missing
    if type(df) == pd.DataFrame:
        df.dropna()

    return df

def start():
    '''
    Start up and display Timelines
    '''
    col_names = ['Event', 'Date', 'Priority']
    # large picture
    mpl.rcParams['figure.dpi'] = 100
    df = import_data_table('Timeline.csv', 1000, col_names)
    # convert dates to standard format if not already
    df = fix_dates_in_col(df, 1, col_names)
    #display timeline
    show_timeline(df, 'Timeline', 100)
    
start()