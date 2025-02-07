from confluent_kafka.avro import AvroConsumer

# Cấu hình Avro Consumer
conf = {
    'bootstrap.servers': '192.168.217.25:9092',
    'schema.registry.url': 'http://192.168.217.25:8081',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = AvroConsumer(conf)
consumer.subscribe(['data_csv'])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        print(f"Received message: {msg.value()}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
