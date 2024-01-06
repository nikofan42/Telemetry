import csv
import time
import irsdk

# Initialize IRSDK
ir = irsdk.IRSDK()
ir.startup()

# Open a CSV file for writing telemetry data
with open('telemetry.csv', 'w', newline='') as csvfile:
    # Define the CSV field names
    fieldnames = [
        'timestamp',
        'Lap',
        'AirDensity',
        'AirPressure',
        'AirTemp',
        'Alt',
        'Brake',
        'BrakeRaw',
        'CpuUsageBG',
        'DCDriversSoFar',
        'DCLapStatus',
        'FrameRate',
        'FuelLevel',
        'FuelLevelPct',
        'FuelUsePerHour',
        'Gear',
        'IsInGarage',
        'IsOnTrack',
        'OnPitRoad',
        'LapBestLap',
        'LapDistPct',
        'Lat',
        'PitSvLRP',
        'PitSvFlags',
        'PitSvFuel',
        'PitSvLFP',
        'PitSvRFP',
        'PitSvRRP',
        'PlayerCarClassPosition',
        'PlayerCarPosition',
        'RaceLaps',
        'SessionFlags',
        'SessionLapsRemain',
        'SessionState',
        'SessionTime',
        'SessionTimeRemain',
        'SessionUniqueID',
        'Speed',
        'TrackTemp',
        'dcABS',
        'dcBrakeBias',
        'dcTractionControl',
        'dcTractionControl2',
        'CarIdxClassPosition',
        'CarIdxEstTime',
        'CarIdxF2Time',
        'CarIdxLap',
        'CarIdxLapDistPct',
        'CarIdxOnPitRoad',
        'CarIdxPosition',
        'CarIdxTrackSurface',
        'WeekendInfo',
        'SessionInfo',
        'QualifyResultsInfo',
        'DriverInfo',
        'SplitTimeInfo',
        # Add any other fields you want to record
    ]

    # Create a CSV writer with the field names as the header row
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Record telemetry data at specific intervals
    for _ in range(6000):  # Record 10 samples; adjust this value as needed
        # Get the telemetry data and write it to the CSV file
        data = {
            'timestamp': time.time(),
            'Lap': ir['Lap'],
            'AirDensity': ir['AirDensity'],
            'AirPressure': ir['AirPressure'],
            'AirTemp': ir['AirTemp'],
            'Alt': ir['Alt'],
            'Brake': ir['Brake'],
            'BrakeRaw': ir['BrakeRaw'],
            'CpuUsageBG': ir['CpuUsageBG'],
            'DCDriversSoFar': ir['DCDriversSoFar'],
            'DCLapStatus': ir['DCLapStatus'],
            'FrameRate': ir['FrameRate'],
            'FuelLevel': ir['FuelLevel'],
            'FuelLevelPct': ir['FuelLevelPct'],
            'FuelUsePerHour': ir['FuelUsePerHour'],
            'Gear': ir['Gear'],
            'IsInGarage': ir['IsInGarage'],
            'IsOnTrack': ir['IsOnTrack'],
            'OnPitRoad': ir['OnPitRoad'],
            'LapBestLap': ir['LapBestLap'],
            'LapDistPct': ir['LapDistPct'],
            'Lat': ir['Lat'],
            'PitSvLRP': ir['PitSvLRP'],
            'PitSvFlags': ir['PitSvFlags'],
            'PitSvFuel': ir['PitSvFuel'],
            'PitSvLFP': ir['PitSvLFP'],
            'PitSvRFP': ir['PitSvRFP'],
            'PitSvRRP': ir['PitSvRRP'],
            'PlayerCarClassPosition': ir['PlayerCarClassPosition'],
            'PlayerCarPosition': ir['PlayerCarPosition'],
            'RaceLaps': ir['RaceLaps'],
            'SessionFlags': ir['SessionFlags'],
            'SessionLapsRemain': ir['SessionLapsRemain'],
            'SessionState': ir['SessionState'],
            'SessionTime': ir['SessionTime'],
            'SessionTimeRemain': ir['SessionTimeRemain'],
            'SessionUniqueID': ir['SessionUniqueID'],
            'Speed': ir['Speed'],
            'TrackTemp': ir['TrackTemp'],
            'dcABS': ir['dcABS'],
            'dcBrakeBias': ir['dcBrakeBias'],
            'dcTractionControl': ir['dcTractionControl'],
            'dcTractionControl2': ir['dcTractionControl2'],
            'CarIdxClassPosition': ir['CarIdxClassPosition'],
            'CarIdxEstTime': ir['CarIdxEstTime'],
            'CarIdxF2Time': ir['CarIdxF2Time'],
            'CarIdxLap': ir['CarIdxLap'],
            'CarIdxLapDistPct': ir['CarIdxLapDistPct'],
            'CarIdxOnPitRoad': ir['CarIdxOnPitRoad'],
            'CarIdxPosition': ir['CarIdxPosition'],
            'CarIdxTrackSurface': ir['CarIdxTrackSurface'],
            'WeekendInfo': ir['WeekendInfo'],
            'SessionInfo': ir['SessionInfo'],
            'QualifyResultsInfo': ir['QualifyResultsInfo'],
            'DriverInfo': ir['DriverInfo'],
            'SplitTimeInfo': ir['SplitTimeInfo'],
            # Add any other fields you want to record
        }
        writer.writerow(data)

        # Wait for a specified time interval before recording the next sample
        time.sleep(1)  # Adjust this value as needed

# Shutdown IRSDK
ir.shutdown()
