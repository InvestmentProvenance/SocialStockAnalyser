```sql
CREATE TABLE your_database_name.Testing(
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name TEXT NOT NULL,
    Age INT NOT NULL,
    Birthtime DATETIME
) COMMENT = "Made for testing database operations."
```

# Testing db_stock.upload_data:
`db_stock.upload_test()`was ran, and we did see the data get uploaded.