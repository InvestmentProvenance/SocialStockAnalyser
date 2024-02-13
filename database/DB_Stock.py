import pymysql
from datetime import datetime, timedelta
import os
import re
import glob


#db = pymysql.connect(host = 'investdata.c5cwsai4kiot.us-east-1.rds.amazonaws.com',user = 'admin',password ='12345678')

host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
database = os.environ['DB_NAME']
testing = os.environ['TESTING']

#cursor = db.cursor()

def DB_Operation(func):
    def wrap(*args, **kwargs): 
        # Before each DB opertaion we have to establish a connection and then close it after
        try:
            db = pymysql.connect(host=host, user=user, password=password, database=database)
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

@DB_Operation
def upload_Stock(database:pymysql.connect, raw_data):
    cursor = database.cursor()
    insert_sql = """
    INSERT INTO stock_data (timestamp, open, high, low, close, volume, symbol)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_sql, raw_data)
    database.commit()

@DB_Operation
def upload_sns(database:pymysql.connect, raw_data):
    cursor = database.cursor()
    insert_sql = """
    INSERT INTO sns_comments (username, timestamp, body, score, site, symbol)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_sql, raw_data)
    database.commit()


@DB_Operation
def read_Stock(database:pymysql.connect, ticker:str,start_date:datetime,end_date:datetime):   #retrieves last 30 days chronologically ordered
    print("reading")
    start_date = end_date - timedelta(days=30)  # 30 days per month approximation
    cursor = database.cursor()

    # Define the SQL query to select all data from the table
    select_query = "SELECT * FROM stock_data WHERE TimeStamp BETWEEN '{}' AND '{}' AND Symbol = '{}' ORDER BY TimeStamp".format(start_date,end_date,ticker)

    print(select_query)

    # Execute the query
    cursor.execute(select_query)

    # Fetch all the rows (table data)
    table_data = cursor.fetchall()

    # Display the table data
    return table_data

