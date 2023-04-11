import irsdk
import time
import pyrebase
import asyncio
import aiosched
from datetime import date
from telemetry_generator import telemetry_generator
import unittest


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



# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1
    lap_counter = 0
    previousFuelLevel = 0
    in_startup = 1
    pit_flag = 0
    t = time.localtime()
    start_time = time.strftime("%H:%M:%S", t)
    a = 0
    sleeptime = 0.5
    idx = 0
    inPitBox = False
    onPitRoad = False
    pitting = False
    pitLaneTime = 0
    pitBoxTime = 0
    pitCounter = 0
    pitUpdated = False
    myName = ""



# here we check if we are connected to iracing
# so we can retrieve some data
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


# our main loop, where we retrieve data
# and do something useful with it
def pushLapData(state, fuelLevel, fuelLastLap, airTemp, lastLapTimestr, classPos, lap, raceLap, windVel, windDir, sessionTimestr, sessionTimeRemainstr,track, PlayerCarMyIncidentCount, trafficValue, sessionID):
    # data = {"Age": 21, "Name": "Benna", "Employed": True, "Vector": [1, 2, 3, 4]}
    if state.pitUpdated == False:
        data = {
            "Fuel Level": str(fuelLevel),
            "Fuel used": str(fuelLastLap),
            "Air temperature": str(airTemp),
            "Laptime": lastLapTimestr,
            "Position": str(classPos),
            "Laps complete": str(lap).zfill(3),
            "Race laps complete": str(raceLap),
            "Wind velocity": str(windVel),
            "Wind direction": str(windDir),
            "Session time elapsed": str(sessionTimestr),
            "Session time remaining": str(sessionTimeRemainstr),
            "Player car incident amount": str(PlayerCarMyIncidentCount),
            "Current traffic value": str(trafficValue),
            "My name is": str(state.myName)
        }
    else:
        data = {
            "Fuel Level": str(fuelLevel),
            "Fuel used": str(fuelLastLap),
            "Air temperature": str(airTemp),
            "Laptime": lastLapTimestr,
            "Position": str(classPos),
            "Laps complete": str(lap).zfill(3),
            "Race laps complete": str(raceLap),
            "Wind velocity": str(windVel),
            "Wind direction": str(windDir),
            "Session time elapsed": str(sessionTimestr),
            "Session time remaining": str(sessionTimeRemainstr),
            "Player car incident amount": str(PlayerCarMyIncidentCount),
            "Pitlane time": str(round(state.pitLaneTime,2)),
            "Pitbox time": str(round(state.pitBoxTime,2)),
            "Current traffic value": str(trafficValue),
            "My name is": str(state.myName)
        }
        state.pitUpdated = False
    timestamp = date.today()


    db.child("races").child(sessionID).child(state.myName).set(data)
    #db.push(data)


def loop(ir):
    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    if state.in_startup == 1:
        state.in_startup = 0
        #print(ir['DriverInfo']['DriverCarIdx'])
        state.idx = ir['DriverInfo']['DriverCarIdx']
        state.previousFuelLevel = ir['FuelLevel']

        driversData = ir['DriverInfo']['Drivers']
        driversNames = {}
        for driver in driversData:
            car_idx = driver['CarIdx']
            name = driver['UserName']
            driversNames[car_idx] = name

        state.myName = driversNames[state.idx]
        sessionID = ir['WeekendInfo']['SessionID']



    def SFget(ir):

        track = ir['WeekendInfo']['TrackName']
        fuelLevel = round(ir['FuelLevel'],2)
        fuelLastLap = round(state.previousFuelLevel - fuelLevel,2)
        airTemp = round(ir['AirTemp'],1)
        lastLapTime = ir['LapLastLapTime']
        #min =
        lastLapTimestr = str(int(lastLapTime // 60)).zfill(2) + ":"\
                         + str(int(lastLapTime - ((lastLapTime // 60)*60))).zfill(2) + "."\
                         + str(round(lastLapTime-int(lastLapTime),4))[2:-1]
        last3LapsTimes = ir['LapLastNLapTime']
        classPos = ir['PlayerCarClassPosition']
        raceLap = ir['RaceLaps']
        windDir = round(ir['WindDir'])
        windVel = round(ir['WindVel'])
        sessionTime = ir['SessionTime']
        sessionTimestr = str(int(sessionTime // 3600)).zfill(2) + ":"\
                         + str(int((sessionTime - sessionTime //3600 * 3600)//60)).zfill(2) + ":" \
                         + str(int(sessionTime-((sessionTime//60)*60))).zfill(2)
        sessionTimeRemain = ir['SessionTimeRemain']
        sessionTimeRemainstr = str(int(sessionTimeRemain // 3600)).zfill(2) + ":"\
                         + str(int((sessionTimeRemain - sessionTimeRemain //3600 * 3600)//60)).zfill(2) + ":" \
                         + str(int(sessionTimeRemain-((sessionTimeRemain//60)*60))).zfill(2)
        trafficArray = ir['CarIdxEstTime']
        trafficValue = len([x for x in trafficArray if -3 < x < 10 and x != 0])
        print(trafficArray)
        PlayerCarMyIncidentCount = ir['PlayerCarMyIncidentCount']




        pushLapData(state, fuelLevel, fuelLastLap, airTemp, lastLapTimestr, classPos, lap, raceLap, windVel, windDir, sessionTimestr, sessionTimeRemainstr, track, PlayerCarMyIncidentCount, trafficValue, sessionID)

        print("Fuel remaining " +str(fuelLevel))
        state.previousFuelLevel = fuelLevel
        print("Fuel used " + str(fuelLastLap))
        print("Air temp is " +str(airTemp))
        #print("Laptime was " + str(lastLapTime))
        print("Laptime was " + lastLapTimestr)
        print("Position " + str(classPos))
        print("Laps completed " + str(lap))
        print("Race laps completed " + str(raceLap))
        print("Wind is " + str(windVel) + " " + str(windDir))
        print("Session time elapsed " + str(sessionTimestr))
        print("Session time remaining " + str(sessionTimeRemainstr))
        print("Current incident count " + str(PlayerCarMyIncidentCount))
        print("Current traffic value " + str(trafficValue))
        print("My name is" + state.myName)
        #print(type(last3LapsTimes))

    if ir['CarIdxTrackSurface'][state.idx] == 2 and state.pitting == False:
        state.sleeptime = 0.1
        state.pitting = True
        print("pitting = true")

    lap = ir['Lap']


    if lap != state.lap_counter:
        state.lap_counter = lap
        time.sleep(2)
        SFget()

    elif state.pitting:
        #print(ir['CarIdxTrackSurface'][state.idx])
        if ir['CarIdxTrackSurface'][state.idx] == 3:
            state.sleeptime = 0.5
            state.pitting = False
            print("pitting = false")
        elif state.inPitBox:
            if ir['CarIdxTrackSurface'][state.idx] == 2:
                state.inPitBox = False
                state.pitCounter = state.pitCounter + 1
                print("inpitbox = false")
                state.pitBoxTime =  time.time() -state.pitBoxStartTime
                print(state.pitBoxTime)

        elif state.onPitRoad:
            if ir['CarIdxTrackSurface'][state.idx] == 1:
                state.pitBoxStartTime = time.time()
                state.inPitBox = True
                print("inpitbox = true")
            elif ir['OnPitRoad'] == False:
                state.pitLaneTime = time.time()- state.pitLaneStartTime
                state.onPitRoad = False
                print("onpitroad = false")
                print(state.pitLaneTime)
                state.pitUpdated = True
        elif ir['OnPitRoad']:
            state.pitLaneStartTime = time.time()
            state.onPitRoad = True
            print("onpitroad = true")





    else:
        #print(ir['SessionNum'])
        pass
        #idx = ir['DriverInfo']['DriverCarIdx']
        #print(ir['OnPitRoad'])
        #print(ir['CarIdxTrackSurface'][idx])

def init_prev_lap_numbers(ir):
    global prev_lap_numbers
    prev_lap_numbers = [0] * 64

def init_prev_track_state(ir):
    global prev_track_state
    prev_track_state = [0] * 64

async def main(ir):
    print("in async main")
    init_prev_lap_numbers()

    tasks = []

    for idx in range(len(ir['CarIdxLap'])):
        tasks.append(asyncio.create_task(monitor_lap_changes(idx)))

    await asyncio.gather(*tasks)

prev_lap_numbers = None
async def monitor_lap_changes(idx):
    global prev_lap_numbers
    print("monitoring lap changes")

    airTemp = round(ir['AirTemp'], 1)
    trackTemp = round(ir['TrackTemp'], 1)
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
                                active_session = ir['SessionInfo']['Sessions'][ir['SessionNum']]
                                car = next((car for car in active_session['ResultsPositions'] if car['CarIdx'] == idx),
                                           None)

                                last_time = car['LastTime']
                                local_lap_times.setdefault(car_idx, {})[lap] = last_time

                                # Update competitor data in Firebase Realtime Database using CarIdx
                                races_ref = db.child(f'races/{sessionID}/{state.myName}/competitorData/{CarNumber}/')
                                races_ref.update({
                                    f'/Class': CarClass,
                                    f'/trackName': trackName,
                                    f'{sessionType}/lapTimes/{lap}': last_time,
                                    f'{sessionType}/trackTemp/{lap}': trackTemp,
                                    f'{sessionType}/trackTemp/{lap}': airTemp
                                })

                                # Update AI analysis data in Firebase Realtime Database using UserID
                                AI_analysis_ref = db.child(f'AiDictionary/{user_id}/{CarClass}/{trackName}/{sessionID}/')
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
                loop()
                asyncio.run(main())
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(state.sleeptime)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
