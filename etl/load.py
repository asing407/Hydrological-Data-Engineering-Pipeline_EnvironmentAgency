import sqlite3

def init_db(db_path: str):
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Dimension Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            station_id TEXT PRIMARY KEY,
            name TEXT,
            river_name TEXT,
            latitude REAL,
            longitude REAL
        )
    """)
    
    # Fact Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT,
            parameter TEXT,
            unit TEXT,
            timestamp TEXT,
            value REAL,
            FOREIGN KEY (station_id) REFERENCES stations (station_id),
            UNIQUE(station_id, parameter, timestamp)
        )
    """)
    conn.commit()
    conn.close()

def load_station(db_path: str, station: dict):
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO stations (station_id, name, river_name, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, (station["station_id"], station["name"], station["river_name"], station["latitude"], station["longitude"]))
    conn.commit()
    conn.close()

def load_measurements(db_path: str, measurements: list):
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for m in measurements:
        cur.execute("""
            INSERT OR IGNORE INTO measurements (station_id, parameter, unit, timestamp, value)
            VALUES (?, ?, ?, ?, ?)
        """, (m["station_id"], m["parameter"], m["unit"], m["timestamp"], m["value"]))
    conn.commit()
    conn.close()