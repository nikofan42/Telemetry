import irsdk
import json
import time


class DataCollector:
    def __init__(self, file_path='telemetry_data.json'):
        self.ir = irsdk.IRSDK()
        self.file_path = file_path
        self.data_stream = []
        self.weekend_info_collected = False
        self.last_session_info_time = 0

    def collect_high_frequency_data(self, ir):
        # High-frequency data collection
        current_data = {
            "timestamp": time.time(),
            "session_time": ir['SessionTime'],  # Using SessionTime as a relative timestamp
            "AirDensity": ir['AirDensity'],
            "AirPressure": ir['AirPressure'],
            "AirTemp": ir['AirTemp'],
            "Alt": ir['Alt'],  # Altitude
            "BrakeRaw": ir['BrakeRaw'],
            "Brake": ir['Brake'],
            "CpuUsageBG": ir['CpuUsageBG'],
            "FuelLevel": ir['FuelLevel'],
            "FuelLevelPct": ir['FuelLevelPct'],
            "FuelUsePerHour": ir['FuelUsePerHour'],
            "IsOnTrack": ir['IsOnTrack'],
            "IsOnTrackCar": ir['IsOnTrackCar'],
            "Lap": ir['Lap'],
            "LapBestLap": ir['LapBestLap'],






            "CarIdxTelemetry": {idx: {
                "ClassPosition": ir['CarIdxClassPosition'][idx],
                "EstTime": ir['CarIdxEstTime'][idx],
                "F2Time": ir['CarIdxF2Time'][idx],
                "Gear": ir['CarIdxGear'][idx],
                "Lap": ir['CarIdxLap'][idx],
                "LapDistPct": ir['CarIdxLapDistPct'][idx],
                "OnPitRoad": ir['CarIdxOnPitRoad'][idx],
                "Position": ir['CarIdxPosition'][idx],
                "RPM": ir['CarIdxRPM'][idx],
                "Steer": ir['CarIdxSteer'][idx],
                "TrackSurface": ir['CarIdxTrackSurface'][idx]
            } for idx in range(64)}

        }
        self.data_stream.append(current_data)

    def collect_session_info(self, ir):
        # Collect SessionInfo (once per minute)
        if time.time() - self.last_session_info_time >= 60:
            self.data_stream.append({"timestamp": time.time(), "SessionInfo": ir['SessionInfo']})
            self.last_session_info_time = time.time()

    def save_data_stream(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data_stream, file)

