def process_station(station_raw: dict, station_id: str) -> dict:
    """Transforms raw station JSON into a clean dictionary."""
    return {
        "station_id": station_id,
        "name": station_raw.get("label", "Unknown"),
        "river_name": station_raw.get("riverName", "Unknown"),
        "latitude": station_raw.get("lat"),
        "longitude": station_raw.get("long")
    }

def filter_target_measures(measures_raw: list, target_keywords: list) -> list:
    """Filters the list of all measures down to our specific target parameters."""
    target_measures = []
    for m in measures_raw:
        param_name = m.get("parameterName", "")
        if isinstance(param_name, dict):
            param_name = param_name.get("label", "")
            
        param_name_lower = param_name.lower()
        unit = m.get("unitName", "Unknown")
        
        if any(keyword in param_name_lower for keyword in target_keywords):
            # Combine the parameter name and unit so the database treats them as distinct!
            distinct_parameter_name = f"{param_name} ({unit})"
            
            target_measures.append({
                "measure_id": m.get("@id"),
                "parameter": distinct_parameter_name,
                "unit": unit
            })
    return target_measures

def process_readings(readings_raw: list, station_id: str, parameter: str, unit: str) -> list:
    """Transforms raw readings JSON into a list of clean dictionaries."""
    clean_readings = []
    for r in readings_raw:
        clean_readings.append({
            "station_id": station_id,
            "parameter": parameter,
            "unit": unit,
            "timestamp": r.get("dateTime"),
            "value": r.get("value")
        })
    return clean_readings