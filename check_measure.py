import requests

stations = requests.get("https://environment.data.gov.uk/flood-monitoring/id/stations?_limit=100").json()["items"]

for s in stations:
    measures = s.get("measures", [])
    water = next((m for m in measures if m["parameter"]=="level"), None)
    flow = next((m for m in measures if m["parameter"]=="flow"), None)
    if water and flow:
        w_data = requests.get(water["@id"] + "/readings?_limit=1&_sort=-dateTime").json().get("items")
        f_data = requests.get(flow["@id"] + "/readings?_limit=1&_sort=-dateTime").json().get("items")
        if w_data and f_data:
            print(s["stationReference"], s["label"])