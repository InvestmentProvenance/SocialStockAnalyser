"""Example file for testing docker container"""
import datetime
from datetime import timedelta
from database import data


end_date = datetime.datetime(2022, 4,29)
start_date = end_date - timedelta(days=30)  # 30 days per month approximation
print("start date: ", start_date)
print("end date: ", end_date)
print(data.get_data(ticker='GME',start_time=start_date, end_time=end_date))

#print(f"top secret database password: {os.environ['DATABASE_TOP_SECRET_KEY']}")
print("Hello World!\n")
