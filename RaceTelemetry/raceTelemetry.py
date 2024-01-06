import irsdk
import asyncio
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import datetime

from startup import *
from Classes import State
from iracingDataHandler import *

cred = credentials.Certificate("../auth.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iracingai-default-rtdb.europe-west1.firebasedatabase.app'})
fb_db = firebase_db.reference()

state = State()

def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def init_prev_lap_numbers():
    global prev_lap_numbers
    prev_lap_numbers = [0] * 64

def init_prev_track_state():
    global prev_track_state
    prev_track_state = [0] * 64

async def main():
    init_prev_lap_numbers()

    tasks = []

    for idx in range(len(ir['CarIdxLap'])):
        tasks.append(asyncio.create_task(monitor_lap_changes(idx)))

    await asyncio.gather(*tasks)

prev_lap_numbers = None
async def monitor_lap_changes(idx):
    global prev_lap_numbers

    airTemp = round(ir['AirTemp'], 1)
    trackTemp = round(ir['TrackTemp'], 1)
    sessionID = ir['WeekendInfo']['SessionID']
    trackName = ir['WeekendInfo']['TrackName']
    print(f"SessionID: {sessionID}, TrackName: {trackName}, airTemp: {airTemp}, trackTemp: {trackTemp}")

    local_lap_times = {}

    # Create a dictionary to map CarIdx to UserID
    car_idx_to_user_id = {driver['CarIdx']: driver['UserID'] for driver in ir['DriverInfo']['Drivers']}
    print(f"car_idx_to_user_id: {car_idx_to_user_id}")

    # Find the active session (the one with the highest SessionNum)
    active_session = max(ir['SessionInfo']['Sessions'], key=lambda s: s['SessionNum'])
    sessionType = active_session['SessionName']
    print(f"Active session: {sessionType}")

    driversData = ir['DriverInfo']['Drivers']
    driversNames = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        name = driver['UserName']
        driversNames[car_idx] = name
    print(f"driversNames: {driversNames}")

    driversNumbers = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        CarNumber = str(driver['CarNumber']).replace("'", '"')
        driversNumbers[car_idx] = CarNumber
    print(f"driversNumbers: {driversNumbers}")

    driversCars = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        CarClass = driver['CarPath']
        driversCars[car_idx] = CarClass
    print(f"driversCars: {driversCars}")


    driversRatings = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        CarRating = driver['IRating']
        driversRatings[car_idx] = CarRating
    print(f"driversRating: {driversRatings}")

    teamNames = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        teamName = driver['TeamName']
        teamNames[car_idx] = teamName
    print(f"teamName: {teamNames}")

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
                        CarRating = driversRatings[car_idx]
                        teamName = teamNames[car_idx]
                        airTemp = round(ir['AirTemp'], 1)
                        trackTemp = round(ir['TrackTemp'], 1)

                        # ... (rest of the code)

                        if lap != -2:  # Check if the last_time value is not -1 before updating the database
                            # Check if the lap time has already been recorded for the car's last lap using the local dictionary
                            if car_idx not in local_lap_times or lap not in local_lap_times[car_idx]:
                                # Update the local dictionary with the new lap time
                                await asyncio.sleep(10)
                                # This needs to be refetched as it has not been updated fully when we trigger it for the first time.
                                active_session = ir['SessionInfo']['Sessions'][ir['SessionNum']]
                                car = next((car for car in active_session['ResultsPositions'] if car['CarIdx'] == idx),
                                           None)

                                last_time = car['LastTime'] if car['LastTime'] != -1 else None

                                local_lap_times.setdefault(car_idx, {})[lap] = last_time

                                classPosition = car['ClassPosition']
                                position = car['Position']
                                time = car['Time']



                                #print(CarNumber + "Last lap:" + last_time + " tracktemp: " + trackTemp + " airtemp: " + airTemp)

                                # Update competitor data in Firebase Realtime Database using CarIdx
                                races_ref = fb_db.child(f'racesTest/{sessionID}/{state.myName}/competitorData/{CarNumber} - {teamName}/')
                                races_ref.update({
                                    f'/Class': CarClass,
                                    f'/trackName': trackName,
                                    f'{sessionType}/lapTimes/{lap}': last_time,
                                    f'{sessionType}/trackTemp/{lap}': trackTemp,
                                    f'{sessionType}/airTemp/{lap}': airTemp,
                                    f'{sessionType}/classPosition/{lap}': classPosition,
                                    f'{sessionType}/position/{lap}': position,
                                    f'{sessionType}/time/{lap}': time,
                                    f'{sessionType}/name/{lap}': name,
                                    f'{sessionType}/CarRating/{lap}': CarRating
                                })

                                # Update AI analysis data in Firebase Realtime Database using UserID
                                AI_analysis_ref = fb_db.child(f'AiDictionaryTest/{user_id}/{CarClass}/{trackName}/{sessionID}/')
                                AI_analysis_ref.update({
                                    f'{sessionType}/lapTimes/{lap}': last_time,
                                    f'{sessionType}/trackTemp/{lap}': trackTemp,
                                    f'{sessionType}/airTemp/{lap}': airTemp,
                                    f'{sessionType}/classPosition/{lap}': classPosition,
                                    f'{sessionType}/position/{lap}': position,
                                    f'{sessionType}/time/{lap}': time,
                                    f'{sessionType}/name/{lap}': name,
                                    f'{sessionType}/CarRating/{lap}': CarRating
                                })

                                #print(str(name) + "#" + str(CarNumber) + " latest laptime for lap " + str(lap) + " is: " + str(last_time))

            await asyncio.sleep(state.sleeptime)


if __name__ == '__main__':
    print("ready", end="")
    time.sleep(1)
    print("\r go!")
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()
    #start = time.time()





    #print(type(ir))

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