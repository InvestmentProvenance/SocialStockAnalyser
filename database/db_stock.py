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
            return func(database = db, *args, **kwargs)
        except pymysql.Error as e:
            print(f"Error: {e}")
        finally:
            if db:
                db.close()
                print("Connection closed")
        return None
    return wrap

@db_operation
def upload_data(insert_sql, raw_data, database:pymysql.connect = None):
    """Uploads the passed raw_data to the database, using the given SQL"""
    cursor = database.cursor()
    cursor.executemany(insert_sql, raw_data)
    database.commit()

def upload_stock(raw_data):
    """Uploads stock data to the database. raw_data is a collection of tuples
        of the form (timestamp, open, high, low, close, volume, symbol) """
    insert_sql = """
        INSERT INTO raw_data (timestamp, open, high, low, close, volume, symbol)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    upload_data(insert_sql, raw_data)

def upload_sns(raw_data):
    """Uploads sns data to database""" #TODO: how to format the data?
    insert_sql = """
        INSERT INTO sns_comments (username, timestamp, body, score, site, symbol)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    upload_data(insert_sql, raw_data)

def upload_test():
    """Uploads test_data to the table Testing(Name, Age, Birthtime)"""
    test_data = [("Bob Middlestone", "23", "2000-12-11 12:13:14Z"),
                 ("Puneet Puskás", "0", "2023-02-25 13:57:23Z"),
                 ("Antía Lindholm", "44", "1950-09-30 00:00:00Z")]
    insert_sql = """
        INSERT INTO Testing(Name, Age, Birthtime)
        VALUES (%s, %s, %s)
        """
    upload_data(insert_sql, test_data)

@db_operation
def read_stock(
    ticker:str,
    start_date:datetime,
    end_date:datetime,
    database:pymysql.connect = None):   #retrieves last 30 days chronologically ordered
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


if __name__ == '__main__':
    # upload_test()
    print(read_stock(
        ticker = "GME",
        start_date = datetime(2021, 1, 1),
        end_date = datetime(2021, 1, 30)))
