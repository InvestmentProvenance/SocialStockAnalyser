import numpy as np
import pandas as pd
import pymysql

# Database credentials and details
db_host = 'investdata.c5cwsai4kiot.us-east-1.rds.amazonaws.com'
db_user = 'admin'
db_password = '12345678'
db_name = 'your_database_name'  # Make sure to replace this with your actual database name
ticker_symbol = 'GME'
start_timestamp = '2021-01-01 00:00:00'
end_timestamp = '2021-03-02 00:00:00'

def fetch_stock_data(symbol, start_date, end_date):
    """
    Connect to an AWS RDS instance and fetch stock price data for a specific symbol within a given date range.
    """
    # Establishing the connection
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    
    try:
        with connection.cursor() as cursor:
            query = f"""
            SELECT timestamp, open, high, low, close
            FROM stock_data
            WHERE symbol = '{symbol}' AND timestamp BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY timestamp ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            # Converting to DataFrame
            df = pd.DataFrame(result, columns=['timestamp', 'open', 'high', 'low', 'close'])
            return df
    finally:
        connection.close()

def calculate_parkinson_variance(df):
    """
    Calculate the variance of the rate of return using Parkinson's Extreme Value Method.
    """
    # Applying Parkinson's formula to calculate the variance
    df['parkinson_variance'] = (1 / (4 * np.log(2))) * ((np.log(df['high'] / df['low'])) ** 2)

    # Calculate the average variance across all rows to represent the overall period's variance
    overall_variance = df['parkinson_variance'].mean()

    return overall_variance, df

# Fetching the data
df = fetch_stock_data(ticker_symbol, start_timestamp, end_timestamp)

# Calculating the Parkinson variance
overall_variance, df_with_parkinson_variance = calculate_parkinson_variance(df)

print("Parkinson Variance of Rate of Return:", overall_variance)
print(df_with_parkinson_variance.head())
