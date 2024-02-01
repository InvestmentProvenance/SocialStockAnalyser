"""Makes requests to AlphaVantage"""
import os
from datetime import datetime, timedelta
import requests


# Replace these API keys with your own keys from https://www.alphavantage.co/support/#api-key
API_KEYS = ['YYLUN0RB2ER81GFR', 'U2AIMRQSAH58QCP2', '0IJGQ4OJUTZC7W6A', 'N2RS2KZ08K54CEQH',
            'H19BQEDTB2YTBP3O']
SYMBOL = 'GME'
INTERVAL = '5min'



def make_request():
    """Makes a Request to AlphaVantage API and saves to a file"""
    # Calculate the start and end months for the past 60 months
    end_month = datetime.now()
    start_month = end_month - timedelta(days=60 * 30)  # 30 days per month approximation

    # Initialize counters for API keys and calls
    api_key_index = 0
    calls_per_key = 0

    while start_month <= end_month:
        # Format the date in YYYY-MM format
        month_str = start_month.strftime('%Y-%m')

        # Build the URL for the API request
        url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
        f"&symbol={SYMBOL}"
        f"&interval={INTERVAL}"
        f"&apikey={API_KEYS[api_key_index]}"
        f"&outputsize=full"
        f"&datatype=csv&month={month_str}")

        # Send the API request
        r = requests.get(url,timeout=10)

        if r.status_code == 200:
            # Define the path to save the file on the desktop
            desktop_path = os.path.expanduser("~/Desktop/Stockdata")
            file_path = os.path.join(desktop_path, f"alphavantage_data_{month_str}.csv")

            # Save the data to a file on the desktop
            with open(file_path, 'wb') as file:
                file.write(r.content)

            print(f"Data for {month_str} saved to {file_path}")

            # Increment the API key index and reset the calls counter if necessary
            calls_per_key += 1
            if calls_per_key >= 25:
                api_key_index = (api_key_index + 1) % len(API_KEYS)
                calls_per_key = 0
        else:
            print(f"Error: Unable to retrieve data for {month_str}. Status code: {r.status_code}")

        # Move to the previous month
        start_month = start_month + timedelta(days=30)
