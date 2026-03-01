import sqlite3


DB_NAME = "hydrology.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_tables(conn):

    cursor = conn.cursor()

    # ---------- Stations table (dimensions)----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        station_id TEXT PRIMARY KEY,
        name TEXT,
        river TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # ---------- Measurements table (fact) ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id TEXT,
        parameter TEXT,
        value REAL,
        timestamp TEXT,
        FOREIGN KEY (station_id) REFERENCES stations(station_id)
    )
    """)

    conn.commit()