"""Example file for testing docker container"""
import os
import database.DB_Stock as db_stock
from database import Data as data
import datetime
from datetime import timedelta

end_date = datetime.datetime(2022, 4,29)
start_date = end_date - timedelta(days=30)  # 30 days per month approximation
print(data.get_Data(ticker='GME',start_Time=start_date, end_Time=end_date))

#print(f"top secret database password: {os.environ['DATABASE_TOP_SECRET_KEY']}")
print("Hello World!\n")
