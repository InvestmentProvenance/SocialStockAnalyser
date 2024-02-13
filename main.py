"""Example file for testing docker container"""
import os
import database.DB_Stock as db_stock
from database import Data as data
import datetime
from datetime import timedelta

end_date = datetime.datetime(2022, 4,29)
start_date = end_date - timedelta(days=30)  # 30 days per month approximation

test_data = [["user", datetime.datetime(2021,1,1), "comments", 10, "reddit.com", "TEST"], ["user2", datetime.datetime(2022, 1, 2), "comments2", 1, "Googledocs.com", "TEST"]]

db_stock.upload_sns(raw_data = test_data, site="reddit.com",symbol= "TEST")

print("start date: ", start_date)
print("end date: ", end_date)
#print(data.get_Data(ticker='GME',start_Time=start_date, end_Time=end_date))

#print(f"top secret database password: {os.environ['DATABASE_TOP_SECRET_KEY']}")
print("Hello World!\n")
