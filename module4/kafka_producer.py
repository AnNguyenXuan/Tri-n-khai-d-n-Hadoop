from confluent_kafka import Producer
import json

# Hàm callback để xử lý thông báo khi message được gửi
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

# Gửi một số message
try:
    for i in range(10):
        key = f'key{i}'
        
        user_data = {
            "id": i,
            "name": f"John Doe {i}",
            "email": f"{i} john@example.com"
        }
        # Serialize message
        value = json.dumps(user_data)
        # Gửi message
        producer.produce('user', key=key, value=value, callback=delivery_report)

        # Đợi cho các message được gửi
        producer.poll(0)

except Exception as e:
    print(f'Error occurred: {e}')
finally:
    # Đảm bảo gửi tất cả các message còn lại
    producer.flush()
