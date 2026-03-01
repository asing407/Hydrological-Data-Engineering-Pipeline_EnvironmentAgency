import sqlite3
import pandas as pd

conn = sqlite3.connect("hydrology.db")

measurements_df = pd.read_sql("SELECT * FROM measurements ORDER BY timestamp DESC", conn)
print(measurements_df.head())