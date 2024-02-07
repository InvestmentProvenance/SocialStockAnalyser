import datetime
import pandas as pd
import database.DB_Stock as db_stock
from datetime import timedelta

def get_Data(ticker:str, start_Time:datetime, end_Time:datetime) -> pd.DataFrame :
    raw_data = db_stock.read_Stock(ticker=ticker,start_date=start_Time,end_date=end_Time)
    df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def get_Data(ticker:str, start_Time:datetime, end_Time:datetime) -> pd.DataFrame : # returns last 30 days if start date not specified
    start_Time = end_Time - timedelta(days=30)
    raw_data = db_stock.read_Stock(ticker=ticker,start_date=start_Time,end_date=end_Time)
    df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df
