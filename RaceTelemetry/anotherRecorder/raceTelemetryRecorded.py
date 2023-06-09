import time
import pyrebase
import asyncio
import aiosched

from datetime import date
from Classes import *
from simulator import CSV_IRSDK  # Import the CSV_IRSDK class

csv_file = 'telemetry.csv'  # Add the CSV file name
ir = CSV_IRSDK(csv_file)  # Replace the irsdk.IRSDK() instance with the CSV_IRSDK instance

config = {
    "apiKey": "AIzaSyB5-lkeChuEgkJ0UXYbf6WUP33fIBNYVdA",
    "authDomain": "iracingai.firebaseapp.com",
    "databaseURL": "https://iracingai-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "iracingai",
    "databaseURL": "https://iracingai-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "iracingai.appspot.com",
    "messagingSenderId": "536602400542",
    "appId": "1:536602400542:web:17ef9c0bedfcf074209b0f",
    "measurementId": "G-CDHEMNLTZT"
};

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Modify the check_iracing function to always set state.ir_connected to True
def check_iracing():
    global state
    state.ir_connected = True

def init_prev_lap_numbers():
    global prev_lap_numbers
    prev_lap_numbers = [0] * 64

def init_prev_track_state():
    global prev_track_state
    prev_track_state = [0] * 64

async def main():
    init_prev_lap_numbers()

    tasks = []

    while ir.current_index < len(ir.telemetry_data):
        for idx in range(len(ir['CarIdxLap'])):
            tasks.append(asyncio.create_task(monitor_lap_changes(idx)))

        await asyncio.gather(*tasks)

        # Advance to the next row of telemetry data
        ir.next()

prev_lap_numbers = None
async def monitor_lap_changes(idx):
    global prev_lap_numbers

    airTemp = round(float(ir['AirTemp']), 1)
    trackTemp = round(float(ir['TrackTemp']), 1)
    sessionID = ir['WeekendInfo']['SessionID']
    trackName = ir['WeekendInfo']['TrackName']

    local_lap_times = {}

    # Create a dictionary to map CarIdx to UserID
    car_idx_to_user_id = {driver['CarIdx']: driver['UserID'] for driver in ir['DriverInfo']['Drivers']}

    # Find the active session (the one with the highest SessionNum)
    active_session = max(ir['SessionInfo']['Sessions'], key=lambda s: s['SessionNum'])
    sessionType = active_session['SessionName']
    print(sessionType)

    driversData = ir['DriverInfo']['Drivers']
    driversNames = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        name = driver['UserName']
        driversNames[car_idx] = name

    driversNumbers = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        CarNumber = driver['CarNumber']
        driversNumbers[car_idx] = CarNumber

    driversCars = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        CarClass = driver['CarPath']
        driversCars[car_idx] = CarClass

    while True:
        if idx < len(ir['CarIdxLap']):
            lap_number = ir['CarIdxLap'][idx]
            if lap_number != prev_lap_numbers[idx]:
                prev_lap_numbers[idx] = lap_number
                #print(f"Lap change detected for CarIdx {idx}: New lap number is {lap_number}")

                if active_session['ResultsPositions'] is not None:
                    car = next((car for car in active_session['ResultsPositions'] if car['CarIdx'] == idx), None)
                    if car:
                        car_idx = car['CarIdx']
                        user_id = car_idx_to_user_id[car_idx]  # Get the UserID for the current CarIdx
                        lap = ir['CarIdxLap'][car_idx] - 1  # Get the lap number for the current car and increment by 1

                        name = driversNames[car_idx]
                        CarNumber = driversNumbers[car_idx]
                        CarClass = driversCars[car_idx]

                        # ... (rest of the code)

                        if lap != -2:  # Check if the last_time value is not -1 before updating the database
                            # Check if the lap time has already been recorded for the car's last lap using the local dictionary
                            if car_idx not in local_lap_times or lap not in local_lap_times[car_idx]:
                                # Update the local dictionary with the new lap time
                                await asyncio.sleep(10)
                                # This needs to be refetched as it has not been updated fully when we trigger it for the first time.
                                session_num = ir['SessionNum'] if 'SessionNum' in ir.telemetry_data[ir.current_index] else 0
                                active_session = ir['SessionInfo']['Sessions'][session_num]
                                car = next((car for car in active_session['ResultsPositions'] if car['CarIdx'] == idx),
                                           None)

                                last_time = car['LastTime']
                                local_lap_times.setdefault(car_idx, {})[lap] = last_time

                                # Update competitor data in Firebase Realtime Database using CarIdx
                                races_ref = db.child(f'races/{sessionID}/{state.myName}/competitorData2/{CarNumber}/')
                                races_ref.update({
                                    f'/Class': CarClass,
                                    f'/trackName': trackName,
                                    f'{sessionType}/lapTimes/{lap}': last_time,
                                    f'{sessionType}/trackTemp/{lap}': trackTemp,
                                    f'{sessionType}/trackTemp/{lap}': airTemp
                                })

                                # Update AI analysis data in Firebase Realtime Database using UserID
                                AI_analysis_ref = db.child(f'AiDictionary2/{user_id}/{CarClass}/{trackName}/{sessionID}/')
                                AI_analysis_ref.update({
                                    f'{sessionType}/lapTimes/{lap}': last_time,
                                    f'{sessionType}/trackTemp/{lap}': trackTemp,
                                    f'{sessionType}/trackTemp/{lap}': airTemp
                                })

                                #print(str(name) + "#" + str(CarNumber) + " latest laptime for lap " + str(lap) + " is: " + str(last_time))

            await asyncio.sleep(state.sleeptime)

if __name__ == '__main__':
    print("ready", end="")
    time.sleep(1)
    print("\r go!")

    # initializing ir and state
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()

            # if we are, then process data
            if state.ir_connected:
                asyncio.run(main())
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(state.sleeptime)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass