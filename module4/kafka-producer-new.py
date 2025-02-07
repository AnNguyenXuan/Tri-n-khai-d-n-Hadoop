from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
import pandas as pd

# Cấu hình Avro Producer
conf = {
    'bootstrap.servers': '192.168.217.25:9092',
    'schema.registry.url': 'http://192.168.217.25:8081'  # URL Schema Registry
}

# Khởi tạo Avro Producer
producer = AvroProducer(conf)

# Đọc dữ liệu từ CSV
data = pd.read_csv(r'D:\data_engineer_roadmap\file_lưu_trữ\module4\data.csv')

# Gửi từng hàng dữ liệu lên Kafka
for index, row in data.iterrows():
    message = {
        'UserID': row['User ID'],  # Tên trường cần trùng với schema đã đăng ký
        'BatteryCapacity': row['Battery Capacity (kWh)'],  # Đảm bảo đúng tên và kiểu dữ liệu
        'EnergyConsumed': row['Energy Consumed (kWh)']
    }
    try:
        producer.produce(
            topic='data_csv',
            value=message  # Không cần khai báo schema ở đây
        )
        print(f"Sent: {message}")
    except SerializerError as e:
        print(f"Serialization error: {e}")

# Đảm bảo dữ liệu được gửi trước khi đóng producer
producer.flush()
