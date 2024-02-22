"""Provides functionality to download and upload pandas dataframes from the DB"""
import datetime
import pandas as pd
from database import db_stock

def get_data(ticker:str, start_time:datetime, end_time:datetime) -> pd.DataFrame :
    """Retrieves the stock data for the given ticker from the database
      and returns it as a pandas dataframe."""
    raw_data = db_stock.read_stock(ticker=ticker,start_date=start_time,end_date=end_time)
    print("first: ", raw_data[0])
    print("last: ", raw_data[-1])
    df = pd.DataFrame(raw_data,
    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def upload_data(csv_data:pd.DataFrame):
    """Uploads stock data to the database.
      csv_data is a pandas dataframe"""
    data_tuples = [tuple(x) for x in csv_data.to_records(index=False)]
    db_stock.upload_stock(raw_data=data_tuples)


#Reuben's Job:
#TODO: read from database instead of file
def get_sns_data(ticker:str, start_time:datetime, end_time:datetime) -> pd.DataFrame :
    """NOT THE ACTUAL METHOD, JUST A PALCEHOLDER FOR BRIJ TO TEST"""
    df = pd.read_csv("wallstreetbets-posts-and-comments-for-august-2021-comments.csv")
    df['datetime'] = pd.to_datetime(df.created_utc, unit='s').dt.tz_localize('UTC') #get timestamps
    df.set_index('datetime', inplace=True)
    df = df[['body', 'sentiment']] #pick certain columns
    df =  df[df.sentiment.notna()] #extract rows with existing sentiment scores
    
    gme_mentions = df.body.str.contains("GME", case=False)
    gamestop_mentions = df.body.str.contains("gamestop", case=False)
    return df[gamestop_mentions | gme_mentions]



#Brij's Job:
#Series should be indexed by datetimes
def price_volume(ticker:str, start_time:datetime, end_time:datetime) -> pd.Series :
    pass

def chat_volume(ticker:str, start_time:datetime, end_time:datetime, intervals:pd.Timedelta) -> pd.Series :
    pass

#TODO: Add log normal - needs to return pandas series