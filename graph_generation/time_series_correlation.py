"""A module for analysing correlation with respect to a difference between two time series."""
import multiprocessing
import sys
import math
from functools import partial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tqdm
sys.path.insert(1, '/workspaces/SocialStockAnalyser') # Super hacky
from database import data


def __run_individual_correlation(compare_func,
                                series1 : pd.Series,
                                series2 : pd.Series,
                                time_diff : pd.Timedelta):
    """Runs compare function once - used for multiprocessing"""
    s2 = series2.copy()
    s2.index = s2.index + time_diff
    return compare_func(series1, s2)

def pearson_correlation(stock_series: pd.Series, sns_series : pd.Series) -> float :
    """Calculates correlation between stock price and sentiment - Uses stock closing priceb
    Series must have timestamps in ascending order"""

    corresponding_sentiment = [None] * (len(stock_series)-1)
    #fill coreresponding sentiment with weighted average of nearest sns sentiments
    for i, stock_timestamp in enumerate(stock_series.index):
        if i == len(stock_series)-1:
            continue
        relevantsentiments = sns_series[
            pd.to_datetime(stock_timestamp):
            pd.to_datetime(stock_series.index[i+1])]
        if len(relevantsentiments) != 0:
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
            stock_prices[count] = stock_series['open'].iloc[idx]
            count+=1


    perason_correlation=  np.corrcoef(np.row_stack((stock_prices,cleaned_sentiments)))[0][1]
    #TODO: The length should be getting shorters as there is less overlap between social and stock maybe?
    lo, hi = data.confidence_interval(perason_correlation, len(stock_prices))
    return {'corr' : perason_correlation, 'lo' : lo, 'hi' :  hi}




#analysis.py has a method to do this a bit cleaner, but this is more flexible
def time_series_compare(
                         series1 : pd.Series,
                        series2 : pd.Series,
                        time_differences,
                        compare_func = pearson_correlation
                        ):
    """Compares two time series using the given function and returns the result as a np array,
    Gives a dataframe with 'corr', 'lo' and 'hi' columns (at least if you use the pearson_correlation function)"""
    #Maybe will work with other time types not tested yet
    series1.sort_index(inplace=True)
    series2.sort_index(inplace=True)
    partial_individual_correlation = partial(
        __run_individual_correlation,
        compare_func,
        series1,
        series2)
    with multiprocessing.Pool() as pool:
        results = list(tqdm.tqdm(
        pool.imap(partial_individual_correlation, time_differences, 
                  chunksize=math.ceil(len(time_differences)/(multiprocessing.cpu_count()*8))),
                total=len(time_differences),
          desc="Calculating Correlation at Different Offsets"))
        #results = list(tqdm.tqdm(map(partial_individual_correlation, time_differences)))
    return pd.DataFrame(results)






#Example usage
if __name__ == "__main__":
    time_diffs_seconds = list(range(-4000, 4000, 20))
    time_diffs = [pd.Timedelta(seconds=i) for i in time_diffs_seconds]

    sns_data = data.get_sns_data("GME", start_date = pd.to_datetime("2021-01-01"), end_date = pd.to_datetime("2021-01-30"))
    stock_data = data.get_data("GME", start_time = pd.to_datetime("2021-01-01"), end_time = pd.to_datetime("2021-01-30"))
    rolling_correlations = time_series_compare(pearson_correlation, stock_data, sns_data, time_diffs)
    print(rolling_correlations)
    plt.plot(time_diffs_seconds, rolling_correlations['corr'], label = 'Correlation')
    yerr = [rolling_correlations['corr'] - rolling_correlations['lo'], 
        rolling_correlations['hi'] - rolling_correlations['corr']]

    # Plot with error bars
    plt.errorbar(time_diffs_seconds, rolling_correlations['corr'], yerr=yerr, fmt='o', capsize=5, label='Confidence Interval')

    plt.xlabel('Time Difference (seconds)')
    plt.ylabel('Correlation')
    #plt.show()
    plt.savefig("correlation.png")
    