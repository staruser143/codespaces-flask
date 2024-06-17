import sqlite3
import pandas as pd

# Create a connection to an in-memory SQLite database
engine=create

# Create a DataFrame with some data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [4, 1, 2, 3, 5],
    'type': ['bar', 'bar', 'bar', 'bar', 'bar'],
    'name': ['SF', 'Montreal', 'SF', 'Montreal', 'SF']
})

# Write the data to a table in the database
df.to_sql('my_table', conn, if_exists='replace', index=False)

# Now you can query the database as you would with a regular database
df_from_db = pd.read_sql_query('SELECT * FROM my_table where name="Montreal"', conn)

print(df_from_db)