"""A module for analysing correlation with respect to a difference between two time series."""
from database import db_stock
import pandas as pd
import numpy as np
from datetime import datetime 

def time_series_compare(compare_func, 
                        series_1_values, series_1_timestamps, 
                        series_2_values, series_2_timestamps, 
                        time_differences):
    """Compares two time series using the given function and returns the result as a np array"""
    results = np.zeores(len(time_differences))
    for i, time_diff in enumerate(time_differences):
        results[i] = compare_func(
            series_1_values, series_1_timestamps, 
            series_2_values, series_2_timestamps + time_diff)
    return results

def correlation(stock_timestamps : np.array, stock_price : np.array, sns_timestamps : np.array, sns_sentiment : np.array) -> float :
    """Calculates correlation between stock price and sentiment - Must be provided in sorted order"""
    stock_timestamps, stock_price, sns_timestamps, sns_sentiment = np.array(stock_timestamps), np.array(stock_price), np.array(sns_timestamps), np.array(sns_sentiment)
    assert len(stock_timestamps) == len(stock_price) 
    assert len(sns_timestamps) == len(sns_sentiment)
    assert all(stock_timestamps[i] <= stock_timestamps[i+1] for i in range(len(stock_timestamps)-1)), "Must be sorted"
    assert all(sns_timestamps[i] <= sns_timestamps[i+1] for i in range(len(sns_timestamps)-1)), "Must be sorted"

    correpsonding_sentiment = np.zeros(len(stock_timestamps))
    #fill coreresponding sentiment with weighted average of nearest sns sentiments
    for index, stock_time in enumerate(stock_timestamps):
        #find the nearest sentiment time
        nearest_sentiment_index = np.searchsorted(sns_timestamps, stock_time)
        total = 0
        totalweight = 0
        count = 0
        for i in range(-1, 2):
            if i >= 0 and i < len(sns_sentiment):
                weight = 1 / abs(sns_timestamps[nearest_sentiment_index + i] - stock_time)
                total += sns_sentiment[nearest_sentiment_index + i] * weight
                totalweight += weight
                count += 1

        correpsonding_sentiment[index] = sns_sentiment[total/count]
        return np.correlate(stock_price, correpsonding_sentiment)
    

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



if __name__ == "__main__":
    
    sns_data = get_market_sentiment()
    stock_data = db_stock.read_stock("GME", datetime(2021, 1, 1), datetime(2021, 9, 1))

    
    sns_data['timestamp'] = pd.to_datetime(sns_data['datetime'])
    stock_data['timestamp'] = pd.to_datetime(stock_data['timestamp'])
    print(correlation(stock_data['timestamp'], stock_data['close'], sns_data['timestamp'], sns_data['sentiment']))
    print(correlation(stock_data['timestamp'], stock_data['close'], sns_data['timestamp'], sns_data['sentiment']))