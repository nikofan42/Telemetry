import irsdk
import json
import time
from confluent_kafka import Producer, KafkaError
from data_structure import *  # Import the classes from data_structure.py

class DataCollector:
    def __init__(self, ir):
        self.ir = ir
        self.last_high_freq_time = 0
        self.last_lap = 0
        self.last_minute_time = 0

        # Initialize the Kafka producer
        self.kafka_producer = Producer({
            'bootstrap.servers': '192.168.68.108:9092',
            'client.id': 'data_collector'
        })

    def send_to_kafka(self, data):
        self.kafka_producer.poll(0)
        self.kafka_producer.produce('telemetry_topic', key='telemetry', value=json.dumps(data))

    def collect_high_frequency_data(self):
        # Create instances of the relevant classes to collect high-frequency data
        driving_status = DrivingStatus(self.ir)
        engine_status = EngineStatus(self.ir)
        speed_velocity = SpeedVelocity(self.ir)
        steering_wheel_data = SteeringWheelData(self.ir)

        # Combine the data into a single dictionary
        high_freq_data = {
            "DrivingStatus": vars(driving_status),
            "EngineStatus": vars(engine_status),
            "SpeedVelocity": vars(speed_velocity),
            "SteeringWheelData": vars(steering_wheel_data)
        }
        return {"type": "high_freq", "data": high_freq_data}

    def collect_lap_data(self):
        # Collect per-lap data using LapTimingData and other relevant classes
        lap_timing_data = LapTimingData(self.ir)

        # Combine the data into a single dictionary
        lap_data = {
            "LapTimingData": vars(lap_timing_data)
        }
        return {"type": "lap", "data": lap_data}

    def collect_minute_data(self):
        # Check if data is available
        if 'CarClassPosition' not in self.ir or self.ir['CarClassPosition'] is None:
            return None  # or handle it in another appropriate way
        # Collect per-minute data such as EnvironmentalData, CarArrayData, etc.
        environmental_data = EnvironmentalData(self.ir)
        car_array_data = CarArrayData()
        # Example: Adding CarData for each car index (modify as needed)
        for car_idx in range(10):  # Assuming 10 cars for example
            car_data = CarData(self.ir, car_idx)
            car_array_data.add_car_data(car_data)

        # Combine the data into a single dictionary
        minute_data = {
            "EnvironmentalData": vars(environmental_data),
            "CarArrayData": [vars(car) for car in car_array_data.car_data]
        }
        return {"type": "minute", "data": minute_data}

    def collect_data(self):
        if not self.ir.is_initialized or not self.ir.is_connected:
            print("iRacing connection lost. Waiting for reconnection...")
            return  # Skip this data collection cycle
        current_time = time.time()

        if self.ir['SessionTime'] - self.last_high_freq_time >= 0.1:
            high_freq_data = self.collect_high_frequency_data()
            self.send_to_kafka(high_freq_data)
            self.last_high_freq_time = self.ir['SessionTime']

        if self.ir['Lap'] != self.last_lap:
            lap_data = self.collect_lap_data()
            self.send_to_kafka(lap_data)
            self.last_lap = self.ir['Lap']

        if current_time - self.last_minute_time >= 60:
            minute_data = self.collect_minute_data()
            self.send_to_kafka(minute_data)
            self.last_minute_time = current_time

    def run(self):
        while True:
            self.collect_data()

if __name__ == '__main__':
    collector = DataCollector()
    collector.run()
