import sqlite3
import os
from etl.load import init_db, load_station, load_measurements

def test_database_operations():
    test_db = "test_hydrology.db"
    
    # 1. Test Initialization
    init_db(test_db)
    assert os.path.exists(test_db)
    
    # 2. Test Dimension Table Load (Stations)
    mock_station = {
        "station_id": "TEST_01",
        "name": "Mock Station",
        "river_name": "Test River",
        "latitude": 50.0,
        "longitude": -1.0
    }
    load_station(test_db, mock_station)
    
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM stations WHERE station_id = 'TEST_01'")
    assert cur.fetchone()[0] == "Mock Station"
    
    # 3. Test Fact Table Load (Measurements)
    mock_measurements = [{
        "station_id": "TEST_01",
        "parameter": "Conductivity (µS/cm)",
        "unit": "µS/cm",
        "timestamp": "2026-01-01T12:00:00",
        "value": 150.5
    }]
    load_measurements(test_db, mock_measurements)
    
    cur.execute("SELECT value FROM measurements WHERE station_id = 'TEST_01'")
    assert cur.fetchone()[0] == 150.5
    
    # 4. Test Idempotency (Inserting same record shouldn't duplicate)
    load_measurements(test_db, mock_measurements)
    cur.execute("SELECT COUNT(*) FROM measurements WHERE station_id = 'TEST_01'")
    assert cur.fetchone()[0] == 1 
    
    conn.close()
    if os.path.exists(test_db):
        os.remove(test_db)