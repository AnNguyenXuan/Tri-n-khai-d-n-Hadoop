from confluent_kafka import Consumer, KafkaError
import json

# Cấu hình consumer
conf = {
    'bootstrap.servers': '192.168.217.25:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest',
}

# Tạo consumer
consumer = Consumer(conf)
consumer.subscribe(['user'])

# Tiêu thụ dữ liệu
try:
    while True:
        msg = consumer.poll(1.0)  # Chờ 1 giây để nhận message

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Đến cuối partition
                continue
            else:
                print(f'Consumer error: {msg.error()}')
                continue

        try:
            # Deserialize message
            value = json.loads(msg.value().decode('utf-8'))
            print(f'Received message: {value}')
        except json.JSONDecodeError as e:
            print(f'Failed to decode JSON: {e}')

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
