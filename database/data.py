"""Provides functionality to download and upload pandas dataframes from the DB"""
from datetime import datetime
# import datetime
import sys
import numpy as np
import pandas as pd
import db_stock
import math
from statistics import NormalDist
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


#Reuben's Job:
#TODO: read from database instead of file
def get_sns_data(ticker:str, start_date:datetime, end_date:datetime) -> pd.DataFrame:
    """Return a dataframe containing the TextBlob sentiment of comments that refer to a specific 
        ticker within the given timerange. The dataframe contains only a sentiment column, and 
        is indexed and ordered by timestamp."""
    raw_data = db_stock.read_sns(ticker=ticker,start_date=start_date,end_date=end_date)
    df = pd.DataFrame(raw_data,
        columns=['timestamp', 'sentiment'])
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
def price_volume(ticker:str, start_time:datetime, end_time:datetime, intervals: pd.Timedelta = pd.Timedelta(5,"min")) -> pd.Series :
    #generates the price * volume for a given time index with the mean of the open and close in the interval
    data = get_data(ticker, start_time, end_time)#.sort_values(by=['timestamp']) #TODO: Stock data already comes out sorted by timestamp -ab2886
    data = data.groupby(pd.Grouper(level='timestamp', freq=intervals)).agg({'open':'first', 'close':'last', 'low' : 'min','high' : 'max',  'volume' : 'sum', 'symbol' : 'first'})
    #print(data)
    return pd.Series((data.volume*(data.open + data.close)/2),index= data.index).interpolate()
    #TODO fix error due l=low granularity in timeframes when out of market hours, NaN error encountered
#WARNING

#print(price_volume("GME", datetime(2021, 1, 1), datetime(2021, 1, 30), pd.Timedelta(10, "min")))
def naive_time_sentiment_aggregator(ticker:str, start_time:datetime, end_time:datetime, intervals:pd.Timedelta) -> pd.DataFrame :
    data = get_sns_data(ticker, start_time, end_time)
    #print(data)
    #print(data.columns)
    #return data.groupby(pd.Grouper(key='datetime', freq=intervals)).sum()
    return data.groupby(pd.Grouper(level='timestamp', freq=intervals)).sum()

def chat_volume(ticker:str, start_time:datetime, end_time:datetime, intervals: pd.Timedelta = pd.Timedelta(5,"min")) -> pd.Series :
    data = get_sns_data(ticker, start_time, end_time)
    #print(data)
    #print(data)
    #print(data.columns)
    #return data.groupby(pd.Grouper(key='datetime', freq=intervals)).sum()
    return data.groupby(pd.Grouper(level='timestamp', freq=intervals)).count()['sentiment'].squeeze()

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
    # print(price_volume("GME", datetime.datetime(2021, 1, 1), datetime.datetime(2021, 1, 30), pd.Timedelta(10, "min")))
    df = get_sns_data( "GME", start_date = datetime(2021, 1, 1), end_date = datetime(2021, 1, 30))
    print(df)
    
    


def calculate_abs_ln_percentage_return(df):
    """
    Adds a column to the DataFrame calculating the absolute natural logarithm 
    percentage return of (close - open) / open for each row.
    """
    # Calculate the percentage return
    df['ercentage_return'] = ((df['close'] - df['open']) / df['open'])
    
    # Calculate the absolute natural logarithm of the percentage return
    df['abs_ln_percentage_return'] = abs(np.log(df['percentage_return'] + 1))
    
    return df['abs_ln_percentage_return']

def calculate_ln_percentage_return(df):
    """
    Adds a column to the DataFrame calculating the absolute natural logarithm 
    percentage return of (close - open) / open for each row.
    """
    # Calculate the percentage return
    df['percentage_return'] = ((df['close'] - df['open']) / df['open'])
    
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
    The average transaction value is defined as the product of volume and the average price,
    where the average price is the mean of the open and close prices.
    """
    # Calculate the average price as the mean of open and close prices
    df['average_price'] = (df['open'] + df['close']) / 2
    
    # Calculate the average transaction value as volume * average_price
    df['average_transaction_value'] = df['volume'] * df['average_price']
    
    return df['average_transaction_value']