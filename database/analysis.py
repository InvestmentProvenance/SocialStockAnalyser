"""Does statistical analysis"""
from typing import List, Tuple
import datetime
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import numpy as np
import time_series_correlation
#Open charts in new windows

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter #To avoid scientific notation

COMMENTS_DATA = "wallstreetbets-posts-and-comments-for-august-2021-comments.csv"
STOCK_DATA = ""


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