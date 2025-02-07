import requests
import json

schema_registry_url = 'http://192.168.217.25:8081'
subject_name = 'data_csv'

schema = {
    "type": "record",
    "name": "data",
    "fields": [
        {"name": "UserID", "type": "string"},
        {"name": "BatteryCapacity", "type": "float"},
        {"name": "EnergyConsumed", "type": "float"}
    ]
}
# 'User ID', 'Battery Capacity (kWh)', 'Energy Consumed (kWh)',
#        'Charging Duration (hours)', 'Charging Rate (kW)',
#        'Charging Cost (USD)', 'State of Charge (Start %)',
#        'State of Charge (End %)', 'Distance Driven (since last charge) (km)',
#        'Temperature (°C)', 'Vehicle Age (years)'



schema_json = json.dumps({"schema": json.dumps(schema)})

response = requests.post(f"{schema_registry_url}/subjects/{subject_name}/versions", headers={"Content-Type": "application/json"},data=schema_json)

if response.status_code == 200:
    print("Schema registered successfully.")
    print("Chi tiết : ", response.json())
else:
    print(f"Lỗi : {response.status_code}")
    print("Chi tiết : " + response.text)