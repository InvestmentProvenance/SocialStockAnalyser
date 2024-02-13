import datetime
import pandas as pd
import database.DB_Stock as db_stock
from datetime import timedelta

def get_Data(ticker:str, start_Time:datetime, end_Time:datetime) -> pd.DataFrame :
    raw_data = db_stock.read_Stock(ticker=ticker,start_date=start_Time,end_date=end_Time)
    print("first: ", raw_data[0])
    print("last: ", raw_data[-1])
    df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def upload_Data(csv_data:pd.DataFrame):
    data_tuples = [tuple(x) for x in csv_data.to_records(index=False)]
    db_stock.upload_Stock(raw_data=data_tuples)