"""Provides functionality to download and upload pandas dataframes from the DB"""
from datetime import datetime
# import datetime
import sys
from statistics import NormalDist
import math
import numpy as np
import pandas as pd
sys.path.insert(1, '/workspaces/SocialStockAnalyser') 
from database import db_stock
sys.path.insert(1, '/workspaces/SocialStockAnalyser') # Super hacky
#from database import db_stock

def get_data(ticker:str, start_time:datetime, end_time:datetime) -> pd.DataFrame :
    """Retrieves the stock data for the given ticker from the database
      and returns it as a pandas dataframe."""
    raw_data = db_stock.read_stock(ticker=ticker,start_date=start_time,end_date=end_time)
    print("first: ", raw_data[0])
    print("last: ", raw_data[-1])
    df = pd.DataFrame(raw_data,
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def upload_data(csv_data:pd.DataFrame):
    """Uploads stock data to the database.
      csv_data is a pandas dataframe"""
    data_tuples = [tuple(x) for x in csv_data.to_records(index=False)]
    db_stock.upload_stock(raw_data=data_tuples)



def get_sns_data(ticker:str, start_date:datetime, end_date:datetime) -> pd.DataFrame:
    """Return a dataframe containing the TextBlob sentiment of comments that refer to a specific 
        ticker within the given timerange. The dataframe contains only a sentiment column, and 
        is indexed and ordered by timestamp."""
    raw_data = db_stock.read_sns(ticker=ticker,start_date=start_date,end_date=end_date)
    df = pd.DataFrame(raw_data,columns=['timestamp', 'sentiment'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def get_sns_data_transformed(ticker:str, start_date:datetime, end_date:datetime) -> pd.DataFrame:
    """Return a dataframe containing the TextBlob sentiment of comments that refer to a specific 
        ticker within the given timerange. The dataframe contains only a sentiment column, and 
        is indexed and ordered by timestamp."""
    raw_data = db_stock.read_sns(ticker=ticker,start_date=start_date,end_date=end_date)
    df = pd.DataFrame(raw_data,
        columns=['timestamp', 'sentiment'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df['sentiment'].apply(lambda x : 1 + (-2/(1+math.exp(10*(x-0.5)))))
    return df

#Brij's Job:
#Series should be indexed by datetimes
def price_volume(ticker:str, start_time:datetime, end_time:datetime,
                 intervals: pd.Timedelta = pd.Timedelta(5,"min")) -> pd.Series :
    """Generates the price * volume for a given time index with the mean of the open and
    close in the interval"""
    #TODO: Stock data already comes out sorted by timestamp -ab2886
    data = get_data(ticker, start_time, end_time)#.sort_values(by=['timestamp'])
    data = data.groupby(pd.Grouper(level='timestamp', freq=intervals)).agg(
        {'open':'first','close':'last','low':'min','high':'max','volume':'sum','symbol':'first'})
    #print(data)
    return pd.Series((data.volume*(data.open + data.close)/2),index= data.index).interpolate()
    #TODO: fix error due l=low granularity in timeframes when out of market hours,
    #      NaN error encountered

#WARNING

#print(price_volume("GME", datetime(2021, 1, 1), datetime(2021, 1, 30), pd.Timedelta(10, "min")))
def naive_time_sentiment_aggregator(ticker:str, start_time:datetime,
                                    end_time:datetime, intervals:pd.Timedelta=pd.Timedelta(5,"min")
                                    ) -> pd.DataFrame:
    """Sums the chat sentiment within each interval (5mins by default), within the given time
    range and ticker."""
    data = get_sns_data(ticker, start_time, end_time)
    #print(data)
    #print(data.columns)
    #return data.groupby(pd.Grouper(key='datetime', freq=intervals)).sum()
    return data.groupby(pd.Grouper(level='timestamp', freq=intervals)).sum()

def chat_volume(ticker:str, start_time:datetime, end_time:datetime,
                intervals: pd.Timedelta = pd.Timedelta(5,"min")) -> pd.Series :
    """Calculates chat velocity for the given ticker in the given time range. 
    By default, each interval is 5 mins."""
    data = get_sns_data(ticker, start_time, end_time)
    #print(data)
    #print(data)
    #print(data.columns)
    #return data.groupby(pd.Grouper(key='datetime', freq=intervals)).sum()
    return data.groupby(pd.Grouper(level='timestamp', freq=intervals)
                        ).count()['sentiment'].squeeze()

#Testing Function
#print(chat_volume("GME",datetime(2021, 1, 1), datetime(2021, 1, 30),pd.Timedelta(75, "min")))
def log_normal(series : pd.Series) -> pd.Series:
    """Performs log(x_n+1/x_n) on each item"""
    k = series.pct_change(1)
    k.apply(lambda x : np.log(x+1))
    return k

def confidence_interval(correlation:int, sample_number:int, conf_int:int = 0.95)->tuple:
    r_prime = 0.5*math.log((1+correlation)/(1-correlation))
    s_prime = 1/(math.sqrt(sample_number-3))
    standard_dev = NormalDist().inv_cdf((1 + conf_int) / 2.)
    lower_prime = r_prime + (standard_dev*s_prime)
    upper_prime = r_prime - (standard_dev*s_prime)
    upper = math.tanh(upper_prime)
    lower = math.tanh(lower_prime)
    return (upper,lower)

if __name__ =='__main__':
    # print(price_volume("GME", datetime(2021,1,1), datetime(2021, 1, 30), pd.Timedelta(10, "min")))
    test_df = get_sns_data( "GME", start_date = datetime(2021, 1, 1),
                           end_date = datetime(2021, 1, 30))
    print(test_df)

def calculate_abs_ln_percentage_return(df):
    """
    Adds a column to the DataFrame calculating the absolute natural logarithm 
    percentage return of (close - open) / open for each row.
    """
    # Calculate the percentage return
    df['percentage_return'] = (df['close'] - df['open']) / df['open']
    # Calculate the absolute natural logarithm of the percentage return
    df['abs_ln_percentage_return'] = abs(np.log(df['percentage_return'] + 1))
    return df['abs_ln_percentage_return']

def calculate_ln_percentage_return(df):
    """
    Adds a column to the DataFrame calculating the absolute natural logarithm 
    percentage return of (close - open) / open for each row.
    """
    # Calculate the percentage return
    df['percentage_return'] = (df['close'] - df['open']) / df['open']
    # Calculate the absolute natural logarithm of the percentage return
    df['ln_percentage_return'] = np.log(df['percentage_return'] + 1)
    return df['ln_percentage_return']

def calculate_abs_ln_ratio_high_low(df):
    """
    Adds a column to the DataFrame calculating the absolute natural logarithm 
    of the ratio of high to low prices for each row.
    """
    # Calculate the ratio of high to low
    df['high_low_ratio'] = df['high'] / df['low']
    # Calculate the absolute natural logarithm of the high to low ratio
    df['abs_ln_high_low_ratio'] = abs(np.log(df['high_low_ratio']))
    return df

def get_volume(df):
    return df['volume']

def calculate_average_transaction_value(df):
    """
    Calculates the average transaction value for each row in the DataFrame.
    The average transaction value is defined as the product of volumse and the average price,
    where the average price is the mean of the open and close prices.
    """
    # Calculate the average price as the mean of open and close prices
    df['average_price'] = (df['open'] + df['close']) / 2
    # Calculate the average transaction value as volume * average_price
    df['average_transaction_value'] = df['volume'] * df['average_price']
    return df['average_transaction_value']

def get_sns_chat_volume(data: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame containing the chat volume of 5-minute intervals."""
    # Resample the DataFrame to 5-minute intervals and count the number of
    # occurrences in each interval
    chat_volume_series = data.resample('5T').size()
    # Convert the resulting Series to a DataFrame with a 'timestamp' index
    chat_volume_df = chat_volume_series.to_frame(name='chat_volume')
    # Add a timestamp index
    chat_volume_df.index.name = 'timestamp'
    return chat_volume_df

def get_average_sentiment_score(data: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame containing the average sentiment score of 5-minute intervals."""
    # Resample the DataFrame to 5-minute intervals and calculate the mean sentiment score in each interval
    average_score = data.resample('5T').agg({'sentiment': 'mean'})
    # Rename the column to 'average_sentiment_score'
    average_score.rename(columns={'sentiment': 'average_sentiment_score'}, inplace=True)
    return average_score

# Example usage:
# Assuming 'sns_data' is your DataFrame containing SNS data with a timestamp index
# average_sentiment_score = get_average_sentiment_score(sns_data)
# print(average_sentiment_score)




def categorize_sentiment(sentiment_score: float) -> str:
    """
    Categorize sentiment based on the sentiment score.
    Positive sentiment: score > 0.1
    Negative sentiment: score < -0.1
    Neutral sentiment: -0.1 <= score <= 0.1
    """
    if sentiment_score > 0.1:
        return 'positive'
    elif sentiment_score < -0.1:
        return 'negative'
    else:
        return 'neutral'

def get_sampled_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resample sentiment data to aggregate counts of positive and negative sentiments
    over 5-minute intervals.
    """
    # Apply categorization of sentiment to the 'sentiment' column
    df['sentiment_category'] = df['sentiment'].apply(categorize_sentiment)
    # Resample the DataFrame to 5-minute intervals and aggregate sentiment counts
    sampled_df = df['sentiment_category'].resample('5T').value_counts().unstack(fill_value=0)
    # Rename columns for clarity
    sampled_df.columns = ['positive_sentiment', 'neutral_sentiment', 'negative_sentiment']
    return sampled_df[['positive_sentiment', 'negative_sentiment']]


# Example usage:
# start_date = datetime(2024, 1, 1)
# end_date = datetime(2024, 1, 2)
# ticker = 'AAPL'

# Get sentiment data
# sns_data = get_sns_data(ticker, start_date, end_date)

# # Resample sentiment data for 5-minute intervals
# sampled_sentiment = get_sampled_sentiment(sns_data)
# print(sampled_sentiment)





def calculate_sentiment_difference(sampled_sentiment: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the difference between counts of positive and negative sentiment
    for each 5-minute interval.
    """
    # Calculate the difference between counts of positive and negative sentiment
    sampled_sentiment['sentiment_difference'] = sampled_sentiment['positive_sentiment'] - sampled_sentiment['negative_sentiment']
    return sampled_sentiment[['sentiment_difference']]

# Example usage:
# difference_df = calculate_sentiment_difference(sampled_sentiment)
# print(difference_df)

def dataframe_to_series(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Convert a column of a DataFrame to a Series.
    """
    # Check if the column exists in the DataFrame
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame")

    # Extract the specified column as a Series
    series = df[column]
    
    return series
def series_to_dataframe(series: pd.Series, column_name: str) -> pd.DataFrame:
    """
    Convert a Series to a DataFrame with a specified column name.
    """
    # Create a DataFrame with the Series and specified column name
    df = pd.DataFrame({column_name: series})
    
    return df


def calculate_correlation(series1: pd.Series, series2: pd.Series) -> float:
    """
    Calculate the correlation coefficient between two time series.
    """
    return series1.corr(series2)




def calculate_autocorrelation(df: pd.DataFrame, column1: str, column2: str, lag: int) -> float:
    """
    Calculate the autocorrelation between two columns of a DataFrame at a specified lag.
    """
    # Extract the specified columns as Series
    series1 = df[column1]
    series2 = df[column2]
    
    # Calculate the autocorrelation between the two series at the specified lag
    autocorr = series1.autocorr(other=series2, lag=lag)
    return autocorr


def calculate_autocorrelation_dataframe(df1: pd.DataFrame, column1: str, df2=None, column2=None, max_lag: int = 0) -> pd.DataFrame:
    """
    Calculate the autocorrelation between two columns of a DataFrame up to a maximum lag,
    or between two columns of different DataFrames up to a maximum lag.
    If df2 and column2 are provided, it calculates the autocorrelation between df1[column1] and df2[column2].
    If df2 and column2 are not provided, it calculates the autocorrelation of df1[column1].
    """
    autocorr_values = []
    for lag in range(max_lag + 1):
        if df2 is None or column2 is None:
            autocorr = df1[column1].autocorr(lag=lag)
        else:
            autocorr = df1[column1].autocorr(other=df2[column2].shift(-lag), lag=lag)
        autocorr_values.append(autocorr)
    
    result_df = pd.DataFrame({'Lag': range(max_lag + 1), 'Autocorrelation': autocorr_values})
    return result_df

