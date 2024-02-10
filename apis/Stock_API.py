import os
from datetime import datetime, timedelta
import requests


# Replace these API keys with your own keys from https://www.alphavantage.co/support/#api-key
API_KEYS = ['YYLUN0RB2ER81GFR', 'U2AIMRQSAH58QCP2', '0IJGQ4OJUTZC7W6A', 'N2RS2KZ08K54CEQH',
            'H19BQEDTB2YTBP3O']
SYMBOL = 'GME'
INTERVAL = '5min'



def make_request(start_month:datetime,end_month:datetime):
    """Makes a Request to AlphaVantage API and saves to a file"""

    # Initialize counters for API keys and calls
    api_key_index = 0
    calls_per_key = 0

    current_month = datetime(start_month)
    
    while current_month <= end_month:
        month_str = start_month.strftime('%Y-%m')
        url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
            f"&symbol={SYMBOL}"
            f"&interval={INTERVAL}"
            f"&apikey={API_KEYS[api_key_index]}"
            f"&outputsize=full"
            f"&datatype=csv&month={month_str}")
        r = requests.get(url,timeout=10)
        if r.status_code != 200:
            print(f"Error: Unable to retrieve data for {month_str}. "
            f"Status code: {r.status_code}")
        elif 'rate limit' in r.text: #if rate limit has been reached
            print(f"Error: Unable to retrieve data for {month_str}. "
            f"Daily Rate limit was reached.")
        else:   #success
            print(r.content)
            calls_per_key += 1
            if calls_per_key >= 25:
                api_key_index = (api_key_index + 1) % len(API_KEYS)
                calls_per_key = 0
        start_month = start_month + timedelta(days=30)
    while start_month <= end_month:
        # Format the date in YYYY-MM format
        month_str = start_month.strftime('%Y-%m')
        desktop_path = os.path.expanduser("~/Desktop/Stockdata")
        file_path = os.path.join(desktop_path, f"alphavantage_data_{month_str}.csv")
        if os.path.exists(file_path):
            print(f"Data for {month_str} already saved.")
        else:
            # Build the URL for the API request
            url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
            f"&symbol={SYMBOL}"
            f"&interval={INTERVAL}"
            f"&apikey={API_KEYS[api_key_index]}"
            f"&outputsize=full"
            f"&datatype=csv&month={month_str}")

            # Send the API request
            r = requests.get(url,timeout=10)

            if r.status_code != 200:
                print(f"Error: Unable to retrieve data for {month_str}. "
                f"Status code: {r.status_code}")
            elif 'rate limit' in r.text: #if rate limit has been reached
                print(f"Error: Unable to retrieve data for {month_str}. "
                f"Daily Rate limit was reached.")
            else:
                # Define the path to save the file on the desktop

                # Save the data to a file on the desktop
                with open(file_path, 'wb') as file:
                    file.write(r.content)

                print(f"Data for {month_str} saved to {file_path}")

                # Increment the API key index and reset the calls counter if necessary
                calls_per_key += 1
                if calls_per_key >= 25:
                    api_key_index = (api_key_index + 1) % len(API_KEYS)
                    calls_per_key = 0

        # Move to the previous month
        start_month = start_month + timedelta(days=30)
