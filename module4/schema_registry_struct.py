import requests

# Địa chỉ Schema Registry
schema_registry_url = "http://localhost:8081"
schema_id = 1  # ID của schema bạn muốn xem

# Lấy thông tin cấu trúc schema
response = requests.get(f"{schema_registry_url}/schemas/ids/{schema_id}")

if response.status_code == 200:
    schema_info = response.json()
    print("Thông tin schema:", schema_info)
else:
    print(f"Lỗi: {response.status_code} - {response.text}")
