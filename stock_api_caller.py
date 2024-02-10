"""Makes requests to AlphaVantage"""
import os
from datetime import datetime, timedelta
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

# Replace these API keys with your own keys from https://www.alphavantage.co/support/#api-key
# API_KEYS = ['YYLUN0RB2ER81GFR', 'U2AIMRQSAH58QCP2', '0IJGQ4OJUTZC7W6A', 'N2RS2KZ08K54CEQH',
#             'H19BQEDTB2YTBP3O']
API_KEY = 'YYLUN0RB2ER81GFR'
SYMBOL = 'GME'

def get_stock_data(symbol : str, month_str: str) -> bytes:
    """Makes a Request to AlphaVantage API.
 
    :raises ValueError: if rate limit reached or if the response status isn't 200.
    """
    interval = '5min'
    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
            f"&symbol={symbol}"
            f"&interval={interval}"
            f"&apikey={API_KEY}"
            f"&outputsize=full"
            f"&datatype=csv&month={month_str}")
    # Send the API request
    r = requests.get(url,timeout=10)
    if r.status_code != 200:
        raise RuntimeError(f"Error: Unable to retrieve data for {month_str}. "
        f"Status code: {r.status_code}")
    if 'rate limit' in r.text: #if rate limit has been reached
        raise RuntimeError(f"Error: Unable to retrieve data for {month_str}. "
        f"Daily Rate limit was reached.")
    return r.content

def save_to_file(file_path : str, data : bytes) -> None:
    """Save data to a file on the desktop"""
    with open(file_path, 'wb') as file:
        file.write(data)

def download_symbol_data(symbol : str, end_month:datetime =datetime.now() ,
                         start_month:datetime =None) -> None:
    """
    Downloads data for the givne ticker symbol from the start month to the end month.
    By default, the end_month is set to today and the start month is set to 60 months ago.
    """
    month_num = 60
    days_in_month = 30
    if start_month is None: 
        start_month = end_month - timedelta(days=month_num * days_in_month)

    # Initialize counters for API keys and calls
    # api_key_index = 0
    # calls_per_key = 0
    while start_month <= end_month:
        month_str = start_month.strftime('%Y-%m')
        desktop_path = os.path.expanduser("~")
        file_path = os.path.join(desktop_path, f"alphavantage_data_{symbol}_{month_str}.csv")
        if os.path.exists(file_path):
            logging.info("Data for %s already saved.", month_str)
        else:
            try:
                data = get_stock_data(symbol, month_str)
            except RuntimeError as e:
                logging.info(e)
            else: #if no exceptions occur
                save_to_file(file_path, data)
                logging.debug("Data for %s saved to %s", month_str, file_path)
        # Move to the next month
        start_month = start_month + timedelta(days=30)
        # Increment the API key index and reset the calls counter if necessary
        # calls_per_key += 1
        # if calls_per_key >= 25:
        #     api_key_index = (api_key_index + 1) % len(API_KEYS)
        #     calls_per_key = 0

download_symbol_data("SPCE")
