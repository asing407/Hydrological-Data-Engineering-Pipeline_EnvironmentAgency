from etl.transform import process_station, filter_target_measures, process_readings

def test_process_station():
    raw_data = {
        "label": "HIPPER_PARK ROAD BRIDGE",
        "riverName": "HIPPER",
        "lat": 53.2348,
        "long": -1.43704
    }
    result = process_station(raw_data, "E64999A")
    
    assert result["station_id"] == "E64999A"
    assert result["name"] == "HIPPER_PARK ROAD BRIDGE"
    assert result["latitude"] == 53.2348

def test_filter_target_measures():
    raw_measures = [
        {"@id": "http://id1", "parameterName": "Dissolved Oxygen", "unitName": "mg/L"},
        {"@id": "http://id2", "parameterName": "Water Level", "unitName": "m"}
    ]
    targets = ["oxygen", "conductivity"]
    
    result = filter_target_measures(raw_measures, targets)
    
    # It should find 1 measure and successfully combine the name and unit
    assert len(result) == 1
    assert result[0]["parameter"] == "Dissolved Oxygen (mg/L)"
    assert result[0]["unit"] == "mg/L"

def test_process_readings():
    raw_readings = [
        {"dateTime": "2026-02-24T12:00:00Z", "value": 9.5}
    ]
    result = process_readings(raw_readings, "E64999A", "Dissolved Oxygen (mg/L)", "mg/L")
    
    assert len(result) == 1
    assert result[0]["station_id"] == "E64999A"
    assert result[0]["value"] == 9.5
    assert result[0]["parameter"] == "Dissolved Oxygen (mg/L)"