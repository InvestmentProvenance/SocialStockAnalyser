import requests
import os
from datetime import datetime, timedelta

# Function to generate month range
def month_range(start_date, end_date):
    start_month = datetime.strptime(start_date, '%Y-%m')
    end_month = datetime.strptime(end_date, '%Y-%m')
    while start_month <= end_month:
        yield start_month.strftime('%Y-%m')
        start_month += timedelta(days=32)  # Move to the next month
        start_month = start_month.replace(day=1)

# API Key and Parameters
api_key = 'ZN1R72QNLMVWF7NQ'
symbol = 'GME'
interval = '5min'
start_month = '2020-01'  # Example start month
end_month = '2022-01'  # Example end month

# Define the path to save the files
desktop_path = os.path.expanduser("~/Desktop/Stockdata")
os.makedirs(desktop_path, exist_ok=True)  # Ensure the directory exists

# Iterate through each month in the range
for month in month_range(start_month, end_month):
    # Update URL with the current month
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}&outputsize=full&datatype=csv&month={month}'
    
    # Send the API request
    r = requests.get(url)
    
    if r.status_code == 200:
        file_path = os.path.join(desktop_path, f"alphavantage_data_{symbol}_{month}.csv")
        
        # Save the data to a file
        with open(file_path, 'wb') as file:
            file.write(r.content)
        
        print(f"Data for {month} saved to {file_path}")
    else:
        print(f"Error: Unable to retrieve data for {month}. Status code: {r.status_code}")

print("Data fetching complete.")
