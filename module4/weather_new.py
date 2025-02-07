import requests
import json
from confluent_kafka import Producer

def get_weather(producer):
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hanoi"
    params = {
        "unitGroup": "metric",  # Đơn vị °C
        "key": "KE9ZLEFKWNY9QHQP6BGJEKX87",  # Thay bằng key của bạn
        "contentType": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        send_weather_to_kafka(producer, data)
    else:
        print(f"Lỗi: {response.status_code} - {response.text}")

def send_weather_to_kafka(producer, data):
    city = data['address']
    current = data['currentConditions']
    temp_c = current['temp']  # Thay đổi tên trường
    humidity_percent = current['humidity']  # Thay đổi tên trường
    weather_description = current['conditions']  # Thay đổi tên trường

    # Tạo message dưới dạng JSON với cấu trúc mới
    weather_message = {
        "location": city,
        "weather": {
            "tempC": temp_c,
            "humidityPercent": humidity_percent,
            "weatherDescription": weather_description
        }
    }

    # Serialize message
    value = json.dumps(weather_message)

    # Gửi message đến topic 'user'
    producer.produce('user', key=city, value=value, callback=delivery_report)

    # Đợi cho các message được gửi
    producer.poll(0)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

# Cấu hình producer
conf = {
    'bootstrap.servers': '192.168.217.25:9092',  # Địa chỉ của Kafka broker
}

# Tạo producer
producer = Producer(conf)

# Gọi hàm để lấy dữ liệu thời tiết và gửi đến Kafka
get_weather(producer)

# Đảm bảo gửi tất cả các message còn lại
producer.flush()
