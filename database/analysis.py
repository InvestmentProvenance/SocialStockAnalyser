"""Temporary file for producing timeseries and derived stats"""
#from typing import List, Tuple
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

def stock_log_normal_parkinson_variance(ticker:str, start_time:datetime, end_time:datetime) -> pd.Series:
    """Calculate the variance of the rate of return using Parkinson's Extreme Value Method."""
    # Applying Parkinson's formula to calculate the variance
    df = data.get_data(ticker, start_time, end_time)
    df['parkinson_variance'] = (1 / (4 * np.log(2))) * ((np.log(df['high'] / df['low'])) ** 2)
    # Calculate the average variance across all rows to represent the overall period's variance
    return df['parkinson_variance']

def chat_velocity(sentiment : pd.Series) -> pd.Series:
    """Group comment count into 5min intervals, returns a Series object"""
    velocity = sentiment.resample('5min').size()
    velocity.name = "Chat Velocity"
    return velocity

def plotSeries(series : pd.Series) -> None:
    """Plots the given series. The series needs to have a datetime index"""
    fig, ax = plt.subplots()

    plt.ticklabel_format(style='plain')
    plot = ax.plot(series, color='red', label=series.name)

    ax.xlabel = 'Time'
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True)) #TODO: Add a y-axis limit at 0?
    ax.set(ylabel=series.name)

    fig.autofmt_xdate(bottom=0.2, rotation=-30, ha='left')
    plt.title(f"{series.name}")
    plt.legend()
    plt.show()

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

def autocorrelate(series: pd.Series) -> pd.Series:
    """Given a pd.Series, calculate autocorrelations upto 100, by shifting the array along by 1.
    Ignores time.
    Returned is a pd.Series, indexed by lag (integer), of the correlation coefficients."""
    data = [(i, series.autocorr(i)) for i in range(100)]
    df = pd.DataFrame(data, columns=['lag', f'{series.name} autocorrelation'])
    return pd.Series(df.set_index('lag').iloc[:, 0])


if __name__ == '__main__':
    # print(stock_log_normal_parkinson_variance("GME", datetime(2021, 1, 1), datetime(2021, 1, 30)))
    print(autocorrelate(data.get_sns_data("GME", datetime(2021, 1, 1), datetime(2021, 1, 30)).sentiment))
    pv = data.price_volume("GME", datetime(2021, 1, 1), datetime(2021, 1, 30))
    sentiment = data.get_sns_data("GME", datetime(2021, 1, 1), datetime(2021, 1, 30)).sentiment
    chat_volume = data.chat_volume("GME", datetime(2021, 1, 1), datetime(2021, 1, 30))
    plotTwoSeries(pv, sentiment)
    plt.savefig("PV vs Sentiment.png")