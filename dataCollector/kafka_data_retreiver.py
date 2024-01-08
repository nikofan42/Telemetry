from kafka import KafkaConsumer

# Kafka consumer configuration
consumer = KafkaConsumer(
    'telemetry_topic',
    bootstrap_servers=['192.168.68.108:9092'],
    auto_offset_reset='earliest'
)

# Print messages from the topic
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")
