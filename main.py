import irsdk
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import datetime

from startup import *
from Classes import State, Firebase
from iracingDataHandler import *



cred = credentials.Certificate("auth.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iracingai-default-rtdb.europe-west1.firebasedatabase.app'})
db = firebase_db.reference()


def loop():

    ir.freeze_var_buffer_latest()



    if state.in_startup == 1:
        start(state, ir)

    lap = ir['Lap']

    checkifpitting(state, ir)
    if lap != state.lap_counter:
            state.lap_counter = lap
            time.sleep(2) #iracing takes a moment to calculate last laptime
            SFget(state, ir, db)



            # do these once a lap
            driversData = ir['DriverInfo']['Drivers']
            driversNames = {}
            for driver in driversData:
                car_idx = driver['CarIdx']
                name = driver['UserName']
                driversNames[car_idx] = name

            state.myName = driversNames[state.idx]
            state.sessionID = ir['WeekendInfo']['SessionID']




def competitorDataFlow():
    # Create a dictionary to map CarIdx to UserID
    car_idx_to_user_id = {driver['CarIdx']: driver['UserID'] for driver in ir['DriverInfo']['Drivers']}
    #print(car_idx_to_user_id)

    print("we are in the competitordataflow now")
    airTemp = round(ir['AirTemp'], 1)
    trackTemp = round(ir['TrackTemp'], 1)
    sessionID = ir['WeekendInfo']['SessionID']
    print(ir['DriverInfo']['DriverCarFuelMaxLtr'])
    #print(sessionID)

    local_lap_times = {}


    driversData = ir['DriverInfo']['Drivers']
    #print(driversData)
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

    # Find the active session (the one with the highest SessionNum)
    active_session = max(ir['SessionInfo']['Sessions'], key=lambda s: s['SessionNum'])
    #print(ir['SessionInfo'])
    #print(ir['SessionInfo']['Sessions'][-1]['SessionType'])
    sessionType = active_session['SessionName']
    print("track state is " + active_session['SessionTrackRubberState'])
    print(sessionType)

    # Process the active session

    print(active_session)
    print(local_lap_times)
    if active_session['ResultsPositions'] is not None:
        #for i in range(len(active_session['ResultsPositions'])):
        #    print(str(i + 1) + ": " + driversNames[active_session['ResultsPositions'][i]['CarIdx']]) # Those who don't have times are not listed

        for car in active_session['ResultsPositions']:
            #print("hmm")
            #time.sleep(1)
            car_idx = car['CarIdx']
            user_id = car_idx_to_user_id[car_idx]  # Get the UserID for the current CarIdx
            lap = ir['CarIdxLap'][car_idx] - 1  # Get the lap number for the current car and increment by 1
            last_time = car['LastTime']
            name = driversNames[car_idx]
            CarNumber = driversNumbers[car_idx]
            CarClass = driversCars[car_idx]

            # ... (rest of the code)
            if lap != -2:  # Check if the last_time value is not -1 before updating the database
                # Check if the lap time has already been recorded for the car's last lap using the local dictionary
                if car_idx not in local_lap_times or lap not in local_lap_times[car_idx]:
                    # Update the local dictionary with the new lap time
                    local_lap_times.setdefault(car_idx, {})[lap] = last_time

                    # Update competitor data in Firebase Realtime Database using CarIdx
                    races_ref = db.child(f'races/{sessionID}/competitorData/{CarNumber}/')
                    races_ref.update({
                        f'/Class': CarClass,
                        f'{sessionType}/lapTimes/{lap}': last_time,
                        f'{sessionType}/trackTemp/{lap}': trackTemp,
                        #f'offTracks/{lap}': lap_off_tracks
                    })

                    # Update AI analysis data in Firebase Realtime Database using UserID
                    AI_analysis_ref = db.child(f'AiDictionary/{user_id}/{CarClass}/{sessionID}/')

                    AI_analysis_ref.update({
                        f'{sessionType}/lapTimes/{lap}': last_time,
                        f'{sessionType}/trackTemp/{lap}': trackTemp,
                        #f'offTracks/{lap}': lap_off_tracks
                    })

                    print(str(name) + "#" + str(CarNumber) + " latest laptime for lap " + str(lap) + " is: " + str(last_time))
        #print(local_lap_times)











if __name__ == '__main__':
    print("ready", end="")
    time.sleep(1)
    print("\r go!")

    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()
    #start(state, ir)
    #print(state.debug)
    #start = time.time()





    #print(type(ir))

    try:
        # infinite loop

        while True:

            # check if we are connected to iracing
            check_iracing(state, ir)

            # if we are, then process data
            if state.ir_connected:
                loop()
                #competitorDataFlow()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(state.sleeptime)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
