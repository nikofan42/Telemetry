import irsdk
import time
import pyrebase
from datetime import date


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
def push(state, fuelLevel, fuelLastLap, airTemp, lastLapTimestr, classPos, lap, raceLap, windVel, windDir, sessionTimestr, sessionTimeRemainstr,track, PlayerCarMyIncidentCount):
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
            "Player car incident amount": str(PlayerCarMyIncidentCount)
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
            "Pitbox time": str(round(state.pitBoxTime,2))
        }
        state.pitUpdated = False
    timestamp = date.today()


    db.child("test").child(track +" " +str(timestamp) + " " + state.start_time).child("Lap " + str(lap-1)).set(data)
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
        state.in_startup = 0
        #print(ir['DriverInfo']['DriverCarIdx'])
        state.idx = ir['DriverInfo']['DriverCarIdx']
        state.previousFuelLevel = ir['FuelLevel']

    #print(len(ir['CarIdxTrackSurface']))
    def SFget():

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

        PlayerCarMyIncidentCount = ir['PlayerCarMyIncidentCount']


        push(state, fuelLevel, fuelLastLap, airTemp, lastLapTimestr, classPos, lap, raceLap, windVel, windDir, sessionTimestr, sessionTimeRemainstr, track, PlayerCarMyIncidentCount)

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
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(state.sleeptime)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
