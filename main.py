import irsdk
import time
import pyrebase
from datetime import date

from startup import *
from Classes import State


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
def pushLapData(state, fuelLevel, fuelLastLap, airTemp, lastLapTimestr, classPos, lap, raceLap, windVel, windDir, sessionTimestr, sessionTimeRemainstr,track, PlayerCarMyIncidentCount, trafficValue, myName, sessionID):
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


    #db.child("races").child(sessionID).child(myName).set(data)#TODO
    db.child("races").child(sessionID).child("niko").set(data)
    #db.push(data)


def loop():
    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    if state.in_startup == 1:
        start(state, ir)
        pass
        #state.in_startup = 0
        #print(ir['DriverInfo']['DriverCarIdx'])
        #state.idx = ir['DriverInfo']['DriverCarIdx']
        #state.previousFuelLevel = ir['FuelLevel']

        #driversData = ir['DriverInfo']['Drivers']
        #driversNames = {}
        #for driver in driversData:
        #    car_idx = driver['CarIdx']
        #    name = driver['UserName']
        #    driversNames[car_idx] = name

        #state.myName = driversNames[state.idx]
        #state.sessionID = ir['WeekendInfo']['SessionID']




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
    print("Direction is")
    print(ir['WindDir'])
    print("Velocity is")
    print(ir['WindVel'])

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




#def pushCompetitorRaceDataDictionary(competitorRaceDataDictionary, sessionID):
#    db.child('races').child(sessionID).child(state.myName).update(competitorRaceDataDictionary)

#def pushCompetitorAiDataDictionary(competitorAiDataDictionary):
#    db.child('AiDictionary').update(competitorAiDataDictionary)


    def SFget(): #why this run on startup

        track = ir['WeekendInfo']['TrackName']
        fuelLevel = round(ir['FuelLevel'],2)
        fuelLastLap = round(state.previousFuelLevel - fuelLevel,2)
        airTemp = round(ir['AirTemp'],1)
        lastLapTime = ir['LapLastLapTime']
        #min =
        lastLapTimestr = str(int(lastLapTime // 60)).zfill(2) + ":"\
                         + str(int(lastLapTime - ((lastLapTime // 60)*60))).zfill(2) + "."\
                         + str(round(lastLapTime-int(lastLapTime),4))[2:-1]
        #last3LapsTimes = ir['LapLastNLapTime'] # not work
        classPos = ir['PlayerCarClassPosition']
        raceLap = ir['RaceLaps']
        windDir = round(ir['WindDir']*180/3.14,1)
        windVel = round(ir['WindVel'],1)
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
        print("hello")
        PlayerCarMyIncidentCount = ir['PlayerCarMyIncidentCount']


        myName = "niko"#TODO

        pushLapData(state, fuelLevel, fuelLastLap, airTemp, lastLapTimestr, classPos, lap, raceLap, windVel, windDir, sessionTimestr, sessionTimeRemainstr, track, PlayerCarMyIncidentCount, trafficValue, myName, sessionID)

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

    # are we pitting

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
            check_iracing()

            # if we are, then process data
            if state.ir_connected:
                loop()
                competitorDataFlow()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(state.sleeptime)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
