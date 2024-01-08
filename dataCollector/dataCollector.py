import irsdk
import json
import time
from confluent_kafka import Producer, KafkaError

class DataCollector:
    def __init__(self, file_path='telemetry_data.json'):
        self.ir = irsdk.IRSDK()
        self.file_path = file_path
        self.data_stream = []
        self.last_lap_time = 0
        self.last_minute_time = 0

        # Initialize the Kafka producer
        self.kafka_producer = Producer({
            'bootstrap.servers': 'localhost:9092',  # Kafka server address
            'client.id': 'data_collector'
        })

    def send_to_kafka(self, data):
        # Produce the data to a Kafka topic
        self.kafka_producer.poll(0)
        self.kafka_producer.produce('telemetry_topic', key='telemetry', value=json.dumps(data))

    def collect_data(self):
        current_time = time.time()

        # Collect high-frequency data 10 times a second
        if self.ir['SessionTime'] - self.last_high_freq_time >= 0.1:
            high_freq_data = self.collect_high_frequency_data()
            self.send_to_kafka(high_freq_data)
            self.last_high_freq_time = self.ir['SessionTime']

        # Collect data once per lap
        if self.ir['Lap'] != self.last_lap:
            lap_data = self.collect_lap_data()
            self.send_to_kafka(lap_data)
            self.last_lap = self.ir['Lap']

        # Collect data once per minute
        if current_time - self.last_minute_time >= 60:
            minute_data = self.collect_minute_data()
            self.send_to_kafka(minute_data)
            self.last_minute_time = current_time

    def collect_high_frequency_data(self):
        # Implement the logic to collect high-frequency data
        return {"type": "high_freq", "data": "sample_high_freq_data"}

    def collect_lap_data(self):
        # Implement the logic to collect per-lap data
        return {"type": "lap", "data": "sample_lap_data"}

    def collect_minute_data(self):
        # Implement the logic to collect per-minute data
        return {"type": "minute", "data": "sample_minute_data"}

    def run(self):
        while True:
            self.collect_data()

if __name__ == '__main__':
    collector = DataCollector()
    collector.run()
