"""An example of how to retrieve data from the Database"""
import os
import pymysql



host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
database = os.environ['DB_NAME']


try:
    # Connect to the MySQL server
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    # Create a cursor object
    cursor = connection.cursor()

    # Define the SQL query to select all data from the table
    select_query = f"SELECT * FROM {'stock_data'}"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all the rows (table data)
    table_data = cursor.fetchall()

    # Display the table data
    for row in table_data:
        print(row)

except pymysql.Error as e:
    print(f"Error: {e}")

finally:
    if connection:
        connection.close()
