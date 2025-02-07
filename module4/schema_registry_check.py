import requests
import json

schema_registry_url = 'http://192.168.217.25:8081'
subject_name = 'user-test'

response = requests.get(f"{schema_registry_url}/subjects/{subject_name}/versions")
if response.status_code == 200:
    print("Các phiên bản schema:", response.json())
else:
    print(f"Lỗi: {response.status_code} - {response.text}")
