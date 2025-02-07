import requests
import json
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def get_weather():
    # url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hanoi?unitGroup=metric&include=hours%2Cdays&key=KE9ZLEFKWNY9QHQP6BGJEKX87&contentType=json"
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hanoi"
    params = {
        "unitGroup": "metric",  # Đơn vị °C
        "key": "KE9ZLEFKWNY9QHQP6BGJEKX87",  # Thay bằng key của bạn
        "contentType": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        value = json.dumps(data)
        producer.produce(topic,key=data['address'],value=value,callback=delivery_report)
        producer.poll(0)
    else:
        print(f"Lỗi: {response.status_code} - {response.text}")

def print_weather(data):
    city = data['address']
    current = data['currentConditions']
    temp = current['temp']
    humidity = current['humidity']
    description = current['conditions']

    print(f"Thời tiết ở {city}:")
    print(f"Nhiệt độ: {temp}°C")
    print(f"Độ ẩm: {humidity}%")
    print(f"Mô tả: {description}")

# Gọi hàm để lấy dữ liệu thời tiết
conf = {
    'bootstrap.servers': '192.168.217.25:9092',
}
topic = 'user'
producer = Producer(conf)
get_weather()
producer.flush()