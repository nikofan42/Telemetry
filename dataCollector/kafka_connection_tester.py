import json
from confluent_kafka import Producer

# If DataCollector class is in a different file or package, import it as well
# from dataCollector import DataCollector
def create_test_producer():
    return Producer({
        'bootstrap.servers': '192.168.68.108:9092',  # Kafka server address
        'client.id': 'test_producer'
    })
def send_test_message(producer):
    def delivery_report(err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    test_data = {"test": "This is a test message"}

    try:
        producer.poll(0)
        producer.produce('telemetry_topic', key='test', value=json.dumps(test_data), callback=delivery_report)
        producer.flush()
        print("Test message sent.")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == '__main__':
    test_producer = create_test_producer()
    send_test_message(test_producer)
