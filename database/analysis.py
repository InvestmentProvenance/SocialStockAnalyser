"""Temporary file for producing timeseries and derived stats"""
from typing import List, Tuple
from datetime import datetime
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import numpy as np
# import time_series_correlation
#Open charts in new windows

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter #To avoid scientific notation
import data
COMMENTS_DATA = "wallstreetbets-posts-and-comments-for-august-2021-comments.csv"
STOCK_DATA = ""

def stock_variance(ticker:str, start_time:datetime, end_time:datetime) -> pd.Series:
    """Returns the stock price variance. Uses only open and close."""
    df = data.get_data(ticker, start_time, end_time)
    df['mean_price'] = (df['open'] + df['close']) / 2
    df['squared_diff'] = (df['open'] - df['mean_price'])**2 + (df['close'] - df['mean_price'])**2
    return df['squared_diff']

def plotTwoSeries(red : pd.Series, blue : pd.Series) -> None:
    """Plots both the given series. Both series need to have an datetime index"""
    fig, red_ax = plt.subplots()
    blue_ax = red_ax.twinx()

    plt.ticklabel_format(style='plain')
    red_plot, = red_ax.plot(red, color='red', label=red.name)
    blue_plot, = blue_ax.plot(blue, color='blue', label=blue.name)

    red_ax.xlabel = 'Time'
    red_ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True)) #TODO: Add a y-axis limit at 0?
    blue_ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    red_ax.set(ylabel=red.name)
    blue_ax.set(ylabel=blue.name)

    fig.autofmt_xdate(bottom=0.2, rotation=-30, ha='left')
    plt.title(f"{red.name} vs {blue.name}")
    plt.legend(handles=[red_plot, blue_plot])
    plt.show()

print(stock_variance("GME", datetime(2021, 1, 1), datetime(2021, 1, 30)))