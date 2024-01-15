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
        geo_data = GeolocationData(self.ir)  # Changed variable name
        orientation_data = OrientationData(self.ir)  # Changed variable name
        in_car_adjustment = InCarAdjustmentsData(self.ir)
        tire_data = TireData(self.ir)



        driver_infos = []
        drivers = []
        if 'DriverInfo' in self.ir and 'Drivers' in self.ir['DriverInfo']:
            for driver_data in self.ir['DriverInfo']['Drivers']:
                driver_info = DriverInfo(driver_data)
                driver = Driver(driver_data)
                driver_infos.append(driver_info)
                drivers.append(driver)

        # Combine the data into a single dictionary
        high_freq_data = {
            "DrivingStatus": vars(driving_status),
            "EngineStatus": vars(engine_status),
            "SpeedVelocity": vars(speed_velocity),
            "SteeringWheelData": vars(steering_wheel_data),
            "GeolocationData": vars(geo_data),  # Use the new variable name
            "OrientationData": vars(orientation_data),  # Use the new variable name
            "InCarAdjustmentsData": vars(in_car_adjustment),
            "TireData": vars(tire_data),
            "DriverInfos": [vars(info) for info in driver_infos],
            "Drivers": [vars(driver) for driver in drivers]
        }

        high_freq_data['timestamp'] = time.time()
        return {"type": "high_freq", "data": high_freq_data}

    def collect_lap_data(self):
        # Collect per-lap data using LapTimingData and other relevant classes
        lap_timing_data = LapTimingData(self.ir)

        # Combine the data into a single dictionary
        lap_data = {
            "LapTimingData": vars(lap_timing_data)
        }
        lap_data['timestamp'] = time.time()
        return {"type": "lap", "data": lap_data}

    def collect_high_frequency_race_data(self):
        print("Entered high-frequency race data collection")
        print(self.ir['CarIdxClassPosition'])
        car_array_data = CarArrayData()

        num_cars = len(self.ir['CarIdxClassPosition'])
        print(f"Number of cars: {num_cars}")

        # Start loop from 1 to skip the safety car at index 0
        for car_idx in range(1, num_cars):
            try:
                #print(f"Processing car index: {car_idx}")
                car_data = CarData(self.ir, car_idx)
                #print(f"CarData created for car index: {car_idx}")
                car_array_data.add_car_data(car_data)
                #print(f"Car data added for car index: {car_idx}")
            except Exception as e:
                print(f"Error processing car index {car_idx}: {e}")

        current_timestamp = time.time()

        # Prepare and send the high frequency race data
        car_data_to_send = {
            "type": "high_freq_race_data",
            "data": [vars(car) for car in car_array_data.car_data],
            "timestamp": current_timestamp
        }

        # Log the data to be sent for debugging
        #print(f"Data to be sent: {car_data_to_send}")

        self.send_to_kafka(car_data_to_send)




    def is_active_car(self, car_idx):
        # Implement logic to check if the car at the given index is active in the session
        # Example: return self.ir['CarIdxClassPosition'][car_idx] is not None and some other condition
        return self.ir['CarIdxClassPosition'][car_idx] is not None  # Add any other conditions as necessary

    def collect_minute_data(self):
        print("Starting minute data collection...")

        try:
            # Collecting basic data (environmental, weekend info, and weekend options)
            environmental_data = EnvironmentalData(self.ir)
            weekend_info = WeekendInfo(self.ir)
            weekend_options = WeekendOptions(self.ir)
            print("Raw WeekendInfo data:", self.ir['WeekendInfo'])

            print("Processing session information...")
            session_data = []
            # Print to check if 'Sessions' is a key in self.ir['SessionInfo']
            print("'Sessions' in self.ir['SessionInfo']: ", 'Sessions' in self.ir['SessionInfo'])
            print("'Sessions in SessionInfo: ", 'Sessions' in self.ir['SessionInfo'])

            for session in self.ir['SessionInfo']['Sessions']:
                session_num = session.get('SessionNum', 'Unknown')
                session_type = session.get('SessionType', 'Unknown')
                print(f"Processing data for Session {session_num} ({session_type})...")
                session_data.append({
                    'SessionNum': session_num,
                    'SessionLaps': session.get('SessionLaps', 'Unknown'),
                    'SessionTime': session.get('SessionTime', 'Unknown'),
                    'SessionNumLapsToAvg': session.get('SessionNumLapsToAvg', 'Unknown'),
                    'SessionType': session_type,
                    'SessionTrackRubberState': session.get('SessionTrackRubberState', 'Unknown'),
                    'SessionName': session.get('SessionName', 'Unknown'),
                    'SessionSubType': session.get('SessionSubType', 'Unknown'),
                    'SessionSkipped': session.get('SessionSkipped', 'Unknown'),
                    'SessionRunGroupsUsed': session.get('SessionRunGroupsUsed', 'Unknown'),
                    'SessionEnforceTireCompoundChange': session.get('SessionEnforceTireCompoundChange', 'Unknown'),
                    'ResultsPositions': session.get('ResultsPositions', []),
                    'ResultsFastestLap': session.get('ResultsFastestLap', []),
                    'ResultsAverageLapTime': session.get('ResultsAverageLapTime', 'Unknown'),
                    'ResultsNumCautionFlags': session.get('ResultsNumCautionFlags', 'Unknown'),
                    'ResultsNumCautionLaps': session.get('ResultsNumCautionLaps', 'Unknown'),
                    'ResultsNumLeadChanges': session.get('ResultsNumLeadChanges', 'Unknown'),
                    'ResultsLapsComplete': session.get('ResultsLapsComplete', 'Unknown'),
                    'ResultsOfficial': session.get('ResultsOfficial', 'Unknown'),
                    # Add any additional session attributes here
                })
                print("Session data processed.")
            # Preparing minute data with all collected information
            minute_data = {
                "EnvironmentalData": vars(environmental_data),
                "WeekendInfo": vars(weekend_info),
                "WeekendOptions": vars(weekend_options),
                "SessionData": session_data,
                "timestamp": time.time()
            }
            print("Minute data collected successfully.")
            return {"type": "minute", "data": minute_data}

        except Exception as e:
            print(f"Error in collect_minute_data: {e}")
            return None

    def collect_data(self):
        # print("Collecting data...")  # Uncomment this if you want to print it every loop iteration

        if not self.ir.is_initialized or not self.ir.is_connected:
            print("iRacing connection lost. Waiting for reconnection...")
            return  # Skip this data collection cycle

        current_time = time.time()

        # Collecting high-frequency data
        #print("Collecting high-frequency data...")
        #high_freq_data = self.collect_high_frequency_data()
        #self.send_to_kafka(high_freq_data)

        # Collecting lap data
        if self.ir['Lap'] != self.last_lap:
            print("Collecting lap data...")
            lap_data = self.collect_lap_data()
            self.send_to_kafka(lap_data)
            self.last_lap = self.ir['Lap']

        # Collecting minute data
        if current_time - self.last_minute_time >= 60:
            print("Collecting minute data...")
            minute_data = self.collect_minute_data()
            if minute_data is not None:
                self.send_to_kafka(minute_data)
            self.last_minute_time = current_time

        if current_time - self.last_high_freq_time >= 0.1:
            print("Collecting high-frequency race data...")
            self.last_high_freq_time = current_time
            self.collect_high_frequency_race_data()

    def run(self):
        while True:
            self.collect_data()


