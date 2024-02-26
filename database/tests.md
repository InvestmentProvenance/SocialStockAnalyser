# Database/
## db_stock.py
DDL for the `Testing` table
```sql
    CREATE TABLE your_database_name.Testing(
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name TEXT NOT NULL,
        Age INT NOT NULL,
        Birthtime DATETIME
    ) COMMENT = "Made for testing database operations."
```

### upload_data()
`db_stock.upload_test()`was ran, and we did see the data get uploaded.

### read_data()
`db_stock.read_test()` was run. We did see the expected output.

### comment_tickers()
The expected output of `['AMC', 'GME', 'NIO']` was returned.

### stock_tickers()
The expected output of `['GME']` was returned.

### social_media_sites()
The expected output of `['investors.hub', 'reddit.com']` was returned.

## data.py

### Testing data.get_sns_data()
```python 
  from datetime import datetime 
  from database.data import get_sns_data
  df = get_sns_data(ticker="GME", start_date = datetime(2021, 1, 1), end_date = datetime(2021, 1, 30))
```
This code was run. `df` was found to be a 37,708 row x 1 col dataframe, indexed and ordered by timestamp, with a sentiment columns.
This code essentially runs the following query:
```sql
  SELECT `timestamp`, vadersentiment_pos
  FROM your_database_name.sns_comments
  WHERE `timestamp` BETWEEN '2021-01-01 00:00:00' AND '2021-01-30 00:00:00'
  AND symbol = 'GME'
  ORDER BY `timestamp`
```
