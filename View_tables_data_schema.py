def view_all_tables(database_connection):
    """
    View all tables in the specified database.

    Parameters:
    - database_connection: A pymysql database connection object.

    Returns:
    - A list of table names in the database.
    """
    cursor = database_connection.cursor()

    # Execute SQL query to retrieve all table names
    cursor.execute("SHOW TABLES")

    # Fetch all table names
    tables = [table[0] for table in cursor.fetchall()]

    # Close cursor
    cursor.close()
    print("Tables in the database:")
    for table in tables:
        print(table)


def view_table_data(database_connection, table_name):
    """
    View data from a specified table.

    Parameters:
    - database_connection: A pymysql database connection object.
    - table_name: The name of the table to view data from.

    Returns:
    - A list of tuples representing rows of data from the specified table.
    """
    cursor = database_connection.cursor()

    # Execute SQL query to retrieve data from specified table
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows of data
    data = cursor.fetchall()

    # Close cursor
    cursor.close()

    return data

def print_table_schema(connection):
    """
    Print the schema of all tables in the specified MySQL database.

    Parameters:
    - connection: A pymysql database connection object.

    Returns:
    - None
    """
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Get a list of all tables in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Iterate over each table
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")

            # Get the schema of the current table
            cursor.execute(f"DESCRIBE {table_name}")
            schema = cursor.fetchall()

            # Print the schema
            for column in schema:
                print(f"  {column[0]}: {column[1]}")

            print()

    except pymysql.Error as e:
        print("Error:", e)
    finally:
        # Close the cursor (connection will be closed later)
        cursor.close()
