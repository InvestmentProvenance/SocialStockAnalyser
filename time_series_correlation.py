"""A module for analysing correlation with respect to a difference between two time series."""
from database import data
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt 
import tqdm


def time_series_compare(compare_func,
                         series1 : pd.Series,
                        series2 : pd.Series,
                        time_differences):
    """Compares two time series using the given function and returns the result as a np array"""
    #Maybe will work with other time types not tested yet
    results = np.zeros(len(time_differences))
    for i, time_diff in enumerate(time_differences):
        shifted_series_2 = series2.copy()
        shifted_series_2.index = shifted_series_2.index + time_diff
        results[i] = compare_func(
            series1,
            shifted_series_2)

    return results

def correlation(stock_series: pd.Series, sns_series : pd.Series) -> float :
    """Calculates correlation between stock price and sentiment - Uses stock closing price"""
    
    #assert all(stock_timestamps[i] <= stock_timestamps[i+1] for i in range(len(stock_timestamps)-1)), "Must be sorted"
    #assert all(sns_timestamps[i] <= sns_timestamps[i+1] for i in range(len(sns_timestamps)-1)), "Must be sorted"

    corresponding_sentiment = [None] * (len(stock_series)-1)
    #fill coreresponding sentiment with weighted average of nearest sns sentiments
    for i, stock_timestamp in enumerate(stock_series.index):
        if i == len(stock_series)-1:
            continue
        #TODO: This is inefficent but the better way seems to not work - perhaps to do with types of datetime
        mask = sns_series.index.to_series().between(stock_timestamp, stock_series.index[i+1])
        relevantsentiments = sns_series[mask]
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
    time_diffs_seconds = list(range(-40, 40, 20))
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


    print("Initial Correlation:")
    print(correlation(stock_series, sns_series))


    print("Rolling Correlations:")

    rolling_correlations = time_series_compare(correlation, stock_series, sns_series, time_diffs)
    print(rolling_correlations)
    plt.plot(time_diffs_seconds, rolling_correlations)
    #plt.show()
    plt.savefig("correlation.png")
    