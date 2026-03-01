import sqlite3
import pandas as pd

def view_data():
    db_path = "hydrology.db"
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    print("--- STATIONS (DIMENSION TABLE) ---")
    stations_df = pd.read_sql_query("SELECT * FROM stations", conn)
    print(stations_df.to_markdown(index=False))
    
    print("\n--- RECENT MEASUREMENTS (FACT TABLE) ---")
    # Let's just look at the 10 most recent measurements
    measurements_df = pd.read_sql_query("SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 10", conn)
    print(measurements_df.to_markdown(index=False))

    print("\n--- MEASUREMENT COUNTS BY PARAMETER ---")
    counts_df = pd.read_sql_query("""
        SELECT parameter, COUNT(*) as total_readings 
        FROM measurements 
        GROUP BY parameter
    """, conn)
    print(counts_df.to_markdown(index=False))

    conn.close()

if __name__ == "__main__":
    view_data()