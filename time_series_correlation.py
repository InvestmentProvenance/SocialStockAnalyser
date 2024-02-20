"""A module for analysing correlation with respect to a difference between two time series."""
from database import data
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt 
import tqdm
import multiprocessing
from functools import partial

def __run_individual_correlation(compare_func, series1 : pd.Series, series2 : pd.Series, time_diff : pd.Timedelta):
    """Runs compare function once - used for multiprocessing"""
    s2 = series2.copy()
    s2.index = s2.index + time_diff
    return compare_func(series1, s2)

def time_series_compare(compare_func,
                         series1 : pd.Series,
                        series2 : pd.Series,
                        time_differences):
    """Compares two time series using the given function and returns the result as a np array"""
    #Maybe will work with other time types not tested yet
    series1.sort_index(inplace=True)
    series2.sort_index(inplace=True)
    partial_individual_correlation = partial(__run_individual_correlation, compare_func, series1, series2)
    with multiprocessing.Pool() as pool:
        results = list(tqdm.tqdm(
        pool.imap(partial_individual_correlation, time_differences)
        , total=len(time_differences), desc="Calculating Correlation at Different Offsets"))
    #results = list(map(partial_individual_correlation, time_differences))

    return np.array(results)


def correlation(stock_series: pd.Series, sns_series : pd.Series) -> float :
    """Calculates correlation between stock price and sentiment - Uses stock closing priceb
    Series must have timestamps in ascending order"""
    
    corresponding_sentiment = [None] * (len(stock_series)-1)
    #fill coreresponding sentiment with weighted average of nearest sns sentiments
    for i, stock_timestamp in enumerate(stock_series.index):
        if i == len(stock_series)-1:
            continue
        relevantsentiments = sns_series[pd.to_datetime(stock_timestamp):pd.to_datetime(stock_series.index[i+1])]
        if (len(relevantsentiments) != 0):
            corresponding_sentiment[i] = np.mean(relevantsentiments)
        elif i != 0:
            corresponding_sentiment[i] = corresponding_sentiment[i-1]

    #figure out size of arrays we need to allocate
    non_null_sentiments_count = 0
    for sentiment in corresponding_sentiment:
        if sentiment is not None:
            non_null_sentiments_count += 1
    stock_prices = np.zeros(non_null_sentiments_count)
    cleaned_sentiments = np.zeros(non_null_sentiments_count)
    count = 0
    for idx, sentiment in enumerate(corresponding_sentiment):
        if  sentiment is not None:
            cleaned_sentiments[count] = corresponding_sentiment[idx]
            stock_prices[count] = stock_series.iloc[idx]
            count+=1
    #TODO: use a different formula for correlation
    return np.correlate(stock_prices, cleaned_sentiments)


#For testing - delete later
def get_market_sentiment():
    """Returns a dataframe of the commment table. It has the timestamp, comment body and sentiment scores.
    Records without a """
    df = pd.read_csv("wallstreetbets-posts-and-comments-for-august-2021-comments 1.csv")
    df['datetime'] = pd.to_datetime(df.created_utc, unit='s').dt.tz_localize('UTC') #get timestamps
    df = df[['datetime', 'body', 'sentiment']] #pick certain columns
    df =  df[df.sentiment.notna()] #extract rows with existing sentiment scores
    
    gme_mentions = df.body.str.contains("GME", case=False)
    gamestop_mentions = df.body.str.contains("gamestop", case=False)
    return df[gamestop_mentions | gme_mentions]


#Example usage
if __name__ == "__main__":
    time_diffs_seconds = list(range(-4000, 4000, 20))
    time_diffs = [pd.Timedelta(seconds=i) for i in time_diffs_seconds]

    sns_data = get_market_sentiment()
    sns_data['timestamp'] = pd.to_datetime(sns_data['datetime']) # TZ aware
    lower_ts = min(sns_data['timestamp'])
    upper_ts = max(sns_data['timestamp'])
    stock_data = data.get_data("GME", lower_ts, upper_ts)

    stock_data['timestamp'] = pd.to_datetime(stock_data['timestamp'], utc = True) # Not TZ aware, I guess I'm assuming UTC
    #sns_timestamps =np.flip( sns_data['timestamp'])
    #sns_sentiment = np.flip( sns_data['sentiment'])

    stock_series = stock_data.set_index('timestamp').close
    sns_series = sns_data.set_index('timestamp').sentiment


    #print("Initial Correlation:")
    #print(correlation(stock_series, sns_series))


    print("Rolling Correlations:")

    rolling_correlations = time_series_compare(correlation, stock_series, sns_series, time_diffs)
    print(rolling_correlations)
    plt.plot(time_diffs_seconds, rolling_correlations)
    #plt.show()
    plt.savefig("correlation.png")
    