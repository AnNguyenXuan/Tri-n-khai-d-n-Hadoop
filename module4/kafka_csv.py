from confluent_kafka import Producer
import pandas as pd
import json

def on_send_success(record_metadata):
    print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

def on_send_error(excp):
    print(f"Error: {excp}")

# Cấu hình Kafka Producer
conf = {
    'bootstrap.servers': '192.168.217.25:9092'  # Đúng cú pháp cho Confluent Kafka
}

producer = Producer(**conf)

# Đọc dữ liệu từ CSV
data = pd.read_csv('/home/nguyenxuanan/data.csv')

# Gửi từng hàng dữ liệu lên Kafka
for index, row in data.iterrows():
    message = json.dumps(row.to_dict()).encode('utf-8')  # Phải tự encode JSON
    producer.produce(
        topic='data_csv',
        value=message,
        callback=lambda err, msg: on_send_success(msg) if not err else on_send_error(err)
    )

# Đảm bảo dữ liệu được gửi trước khi đóng producer
producer.flush()
print("Tất cả dữ liệu đã được gửi thành công!")
