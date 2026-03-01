import requests
import datetime

API_BASE = "https://environment.data.gov.uk/hydrology/id"

def get_station_info(station_id: str) -> dict:
    """Fetches station metadata."""
    url = f"{API_BASE}/stations/{station_id}.json"
    response = requests.get(url)
    response.raise_for_status()
    items = response.json().get("items", [])
    return items[0] if isinstance(items, list) and items else items

def get_station_measures(station_id: str) -> list:
    """Fetches all available measurement parameters for a station."""
    url = f"{API_BASE}/measures.json?station.notation={station_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("items", [])

def get_measure_readings(measure_url: str, limit: int = 10) -> list:
    """Fetches the N most recent readings for a specific measure."""
    # changed from &_sorted to &_sort=-date
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    url = f"{measure_url}/readings.json?mineq-date={start_date}&_sort=-date&_limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("items", [])