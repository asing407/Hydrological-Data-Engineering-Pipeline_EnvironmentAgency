import logging
import requests  # <-- Add this line
from etl.extract import get_station_info, get_station_measures, get_measure_readings
from etl.transform import process_station, filter_target_measures, process_readings
from etl.load import init_db, load_station, load_measurements

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    # 'E64999A' is the API notation for HIP860PER_PARK ROAD BRIDGE_E_202312
    STATION_ID = "E64999A" 
    DB_PATH = "hydrology.db"
    TARGET_KEYWORDS = ["oxygen", "conductivity"]
    
    logging.info("Initializing Database...")
    init_db(DB_PATH)
    
    logging.info(f"Extracting data for station {STATION_ID}...")
    station_raw = get_station_info(STATION_ID)
    station_clean = process_station(station_raw, STATION_ID)
    
    logging.info("Loading station data...")
    load_station(DB_PATH, station_clean)
    
    logging.info("Extracting station measures...")
    measures_raw = get_station_measures(STATION_ID)
    target_measures = filter_target_measures(measures_raw, TARGET_KEYWORDS)
    
    all_readings = []
    for tm in target_measures:
        logging.info(f"Fetching 10 most recent readings for: {tm['parameter']}")
        try:
            readings_raw = get_measure_readings(tm["measure_id"], limit=10)
            clean_readings = process_readings(readings_raw, STATION_ID, tm["parameter"], tm["unit"])
            all_readings.extend(clean_readings)
        except requests.exceptions.HTTPError as e:
            logging.error(f"Failed to fetch readings for {tm['parameter']}: {e}")
        
    if all_readings:
        logging.info(f"Loading {len(all_readings)} measurements to database...")
        load_measurements(DB_PATH, all_readings)
    else:
        logging.warning("No readings found for the specified parameters.")
        
    logging.info("Pipeline executed successfully.")

if __name__ == "__main__":
    run_pipeline()