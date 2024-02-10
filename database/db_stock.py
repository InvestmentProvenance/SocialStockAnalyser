"""Provides wrapper for Database Operations"""
from datetime import datetime, timedelta
from typing import Callable
import os
import pymysql



host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
database_name = os.environ['DB_NAME']
testing = os.environ['TESTING']

#cursor = db.cursor()

def db_operation(func: Callable[..., pymysql.connect ]):
    """Decorator to Provide a database connection to the function with named argument 'database'
      and close it after the operation is done. """
    def wrap(*args, **kwargs):
        # Before each DB opertaion we have to establish a connection and then close it after
        try:
            db = pymysql.connect(host=host, user=user, password=password, database=database_name)
            print("trying operation")
            kwargs['database'] = db
            return func(*args, **kwargs)
        except pymysql.Error as e:
            print(f"Error: {e}")
        finally:
            if db:
                db.close()
                print("Connection closed")
        return None
    return wrap

@db_operation
def upload_stock(database:pymysql.connect, raw_data):
    """Uploads stock data to the database. raw_data is a collection of tuples"""
    cursor = database.cursor()
    insert_sql = """
    INSERT INTO stock_data (timestamp, open, high, low, close, volume, symbol)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_sql, raw_data)
    database.commit()

@db_operation
def read_stock(
    database:pymysql.connect,
    ticker:str,
    start_date:datetime,
    end_date:datetime):   #retrieves last 30 days chronologically ordered
    """Retrives the stock data for the given ticker from the database"""
    print("reading")
    start_date = end_date - timedelta(days=30)  # 30 days per month approximation
    cursor = database.cursor()

    # Define the SQL query to select all data from the table
    select_query = (f"SELECT * FROM stock_data WHERE TimeStamp "
    f"BETWEEN '{start_date}' AND '{end_date}' AND Symbol = '{ticker}' ORDER BY TimeStamp")
    print(select_query)

    # Execute the query
    cursor.execute(select_query)

    # Fetch all the rows (table data)
    table_data = cursor.fetchall()

    # Display the table data
    return table_data
