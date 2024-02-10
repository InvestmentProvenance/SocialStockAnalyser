"""Provides functionality to download and upload pandas dataframes from the DB"""
import datetime
import pandas as pd
import db_stock

def get_data(ticker:str, start_Time:datetime, end_Time:datetime) -> pd.DataFrame :
    """Retrieves the stock data for the given ticker from the database and returns it as a pandas dataframe."""
    raw_data = db_stock.read_stock(ticker=ticker,start_date=start_Time,end_date=end_Time)
    print("first: ", raw_data[0])
    print("last: ", raw_data[-1])
    df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def upload_data(csv_data:pd.DataFrame):
    """Uploads stock data to the database. csv_data is a pandas dataframe"""
    data_tuples = [tuple(x) for x in csv_data.to_records(index=False)]
    db_stock.upload_stock(raw_data=data_tuples)