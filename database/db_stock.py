"""Provides wrapper for Database Operations"""
from datetime import datetime, timedelta
from typing import Any, Callable, List, Tuple
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
def upload_data(insert_sql : str, raw_data:List[Tuple[Any, ...]], database:pymysql.connect = None):
    """Uploads the passed raw_data to the database, using the given SQL"""
    cursor = database.cursor()
    cursor.executemany(insert_sql, raw_data)
    database.commit()

def upload_stock(raw_data:List[Tuple[Any, ...]]) -> None:
    """Uploads stock data to the database. raw_data is a collection of tuples
        of the form (timestamp, open, high, low, close, volume, symbol) """
    insert_sql = """
        INSERT INTO stock_data (timestamp, open, high, low, close, volume, symbol)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    upload_data(insert_sql, raw_data)

def upload_sns(raw_data:List[Tuple[Any, ...]]) -> None:
    """Uploads sns data to database""" #TODO: how to format the data?
    insert_sql = """
        INSERT INTO sns_comments (username, timestamp, body, score, site, symbol)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    upload_data(insert_sql, raw_data)

def upload_test() -> None:
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
def read_data(select_query:str, database:pymysql.connect=None) -> Tuple[Tuple[Any, ...]]:
    """Performs the given select_query, and returns the output as a tuple of tuples."""
    print("reading")
    cursor = database.cursor()
    print(select_query)
    # Execute the query
    cursor.execute(select_query)
    # Fetch all the rows (table data)
    table_data = cursor.fetchall()
    return table_data

def read_stock(
    ticker:str,
    start_date:datetime,
    end_date:datetime) -> Tuple[Tuple[Any, ...]]: #This type could be made more stringent.
    """Retrieves the stock data for the given ticker from the database, for the last 30 days,
        chronologically ordered"""
    # start_date = end_date - timedelta(days=30)  # 30 days per month approximation
    # Define the SQL query to select all data from the table
    select_query = (f"SELECT * FROM stock_data WHERE TimeStamp "
        f"BETWEEN '{start_date}' AND '{end_date}' AND Symbol = '{ticker}' ORDER BY TimeStamp")
    return read_data(select_query)

def read_sns(ticker:str, start_date:datetime, end_date:datetime) -> Tuple[Tuple[Any, ...]]:
    """Gets the TextBlob sentiment for the given ticker, between the given dates."""
    #The database column name (vadersentiment_pos) is a misnomer (it actually represents the
    #mixed score of the TextBlob sentiment analyser).
    select_query = f"""
        SELECT `timestamp`, vadersentiment_pos
        FROM sns_comments
        WHERE `timestamp` BETWEEN '{start_date}' AND '{end_date}'
        AND symbol = '{ticker}'
        AND vadersentiment_pos IS NOT NULL
        ORDER BY `timestamp`"""
    return read_data(select_query)

def read_test() -> None:
    """Tests the read_data function."""
    select_query = """SELECT *
        FROM your_database_name.Testing 
        WHERE Birthtime BETWEEN '1999-03-02 14:14:14' AND '2023-02-25 13:57:24'"""
    print(read_data(select_query))

def get_list(select_query : str) -> List[Any]:
    """Return the result of a 1-column SELECT statement, as a list"""
    ticker_list = read_data(select_query)
    return [ticker for (ticker,) in ticker_list] # list comprehension

def comment_tickers() -> List[str]:
    """Returns a list of tickers that appear in the comments"""
    select_query = """
        SELECT DISTINCT symbol
        FROM sns_comments 
        ORDER BY symbol"""
    return get_list(select_query)

def stock_tickers() -> List[str]:
    """Returns a list of tickers that appear in the stock data"""
    select_query = """
        SELECT DISTINCT symbol
        FROM stock_data 
        ORDER BY symbol"""
    return get_list(select_query)

def social_media_sites() -> List[str]:
    """Returns a list of social media sites"""
    select_query = """
        SELECT DISTINCT site
        FROM sns_comments 
        ORDER BY site"""
    return get_list(select_query)

if __name__ == '__main__':
    # upload_test()
    # read_test()
    # print("Stock tickers: ", stock_tickers())
    # print("Comment tickers: ", comment_tickers())
    # print("Sites: ", social_media_sites())
    # print(read_stock(
    #     ticker = "GME",
    #     start_date = datetime(2021, 1, 1),
    #     end_date = datetime(2021, 1, 30)))
    pass
