# get data from iracing and move it around
import datetime
import time


# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing(state, ir):
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


def SFget(state, ir, db):
    print("juhuu")

    track = ir['WeekendInfo']['TrackName']
    #fuelLevel = round(ir['FuelLevel'],2)
    #fuelLastLap = round(state.previousFuelLevel - fuelLevel,2)
    #airTemp = round(ir['AirTemp'],1)
    #lastLapTime = ir['LapLastLapTime']
        #min =
    #lastLapTimestr = str(int(lastLapTime // 60)).zfill(2) + ":"\
     #                    + str(int(lastLapTime - ((lastLapTime // 60)*60))).zfill(2) + "."\
     #                    + str(round(lastLapTime-int(lastLapTime),4))[2:-1]
        #last3LapsTimes = ir['LapLastNLapTime'] # not work
    #classPos = ir['PlayerCarClassPosition']
    #raceLap = ir['RaceLaps']
    #windDir = round(ir['WindDir']*180/3.14,1)
    #windVel = round(ir['WindVel'],1)
    #sessionTime = ir['SessionTime']
    #sessionTimestr = str(int(sessionTime // 3600)).zfill(2) + ":"\
    #                     + str(int((sessionTime - sessionTime //3600 * 3600)//60)).zfill(2) + ":" \
    #                     + str(int(sessionTime-((sessionTime//60)*60))).zfill(2)
    #sessionTimeRemain = ir['SessionTimeRemain']
    #sessionTimeRemainstr = str(int(sessionTimeRemain // 3600)).zfill(2) + ":"\
    #                     + str(int((sessionTimeRemain - sessionTimeRemain //3600 * 3600)//60)).zfill(2) + ":" \
    #                     + str(int(sessionTimeRemain-((sessionTimeRemain//60)*60))).zfill(2)
    trafficArray = ir['CarIdxEstTime']
    trafficValue = len([x for x in trafficArray if -3 < x < 10 and x != 0])
    #print(trafficArray)
    #print("hello")
    #PlayerCarMyIncidentCount = ir['PlayerCarMyIncidentCount']

    #print(ir['LapLastLapTime'])
    #a = 9.28
    #print(str(int(ir['LapLastLapTime'] //60)).zfill(2) + ":" + str(round(ir['LapLastLapTime']\
    #                    - ir['LapLastLapTime'] // 60 *60,3)).ljust(6,'0'))
    #print(str((int(ir['LapLastLapTime'])\
    #                    - int(ir['LapLastLapTime']) // 60 *60)).zfill(2))
    #print(str(round(ir['LapLastLapTime'] % int(ir['LapLastLapTime']),3))[2:])
    if int(ir['LapLastLapTime']) != 0:
        laptime = str(int(ir['LapLastLapTime'] //60)).zfill(2) + ":" + str((int(ir['LapLastLapTime'])\
                        - int(ir['LapLastLapTime']) // 60 *60)).zfill(2) + "." + str(round(ir['LapLastLapTime'] % int(ir['LapLastLapTime']),3))[2:].ljust(3,'0')
    else:
        laptime = "00:00.00"
    SFdata = {
        "Fuel Level": str(round(ir['FuelLevel'],2)),
        "Fuel used": str(round(state.previousFuelLevel - ir['FuelLevel'],2)),
        "Air temperature": str(round(ir['AirTemp'],1)),
        "Laptime": laptime,
        #"Laptime": str(int(ir['LapLastLapTime'] //60)).zfill(2) + ":" + str(round(ir['LapLastLapTime']\
        #                - ir['LapLastLapTime'] // 60 *60,3)).ljust(6,'0'),
        #"Laptime": str(int(ir['LapLastLapTime'] // 60)).zfill(2) + ":"\
        #                 + str(int(ir['LapLastLapTime'] - ((ir['LapLastLapTime'] // 60)*60))).zfill(2) + "."\
        #                 + str(round(ir['LapLastLapTime']-int(ir['LapLastLapTime']),4))[2:-1],
        "Position": str(ir['PlayerCarClassPosition']),
        "Laps complete": str(ir['Lap']).zfill(3),
        "Race laps complete": str(ir['RaceLaps']),
        "Wind velocity": str(round(ir['WindVel'],1)),
        "Wind direction": str(round(ir['WindDir']*180/3.14,1)),
        "Session time elapsed": str(int(ir['SessionTime'] // 3600)).zfill(2) + ":"\
                         + str(int((ir['SessionTime'] - ir['SessionTime'] //3600 * 3600)//60)).zfill(2) + ":" \
                         + str(int(ir['SessionTime']-((ir['SessionTime']//60)*60))).zfill(2),
        "Session time remaining": str(int(ir['SessionTimeRemain'] // 3600)).zfill(2) + ":"\
                         + str(int((ir['SessionTimeRemain'] - ir['SessionTimeRemain'] //3600 * 3600)//60)).zfill(2) + ":" \
                         + str(int(ir['SessionTimeRemain']-((ir['SessionTimeRemain']//60)*60))).zfill(2),
        "Player car incident amount": str(ir['PlayerCarMyIncidentCount']),
        "Pitted last lap": state.pitUpdated,
        "Pitlane time": str(round(state.pitLaneTime, 2)),
        "Pitbox time": str(round(state.pitBoxTime, 2)),
        "Current traffic value": str(trafficValue),
        "My name is": str(state.myName),
        "Timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        "Gap to leader": str(round(ir['CarIdxF2Time'][state.idx], 1)),
        "Fuel tank size": ir['DriverInfo']['DriverCarFuelMaxLtr'],
        "Session name": ir['SessionInfo']['Sessions'][ir['SessionNum']]['SessionName'],
        "Session track state": ir['SessionInfo']['Sessions'][ir['SessionNum']]['SessionTrackRubberState'],
        "SessionID": ir['WeekendInfo']['SessionID']
    }

    if state.pitUpdated:
        state.pitLaneTime = 0
        state.pitBoxTime = 0
        state.pitUpdated = False

    state.previousFuelLevel = ir['FuelLevel']

    db.child("Backend Ingest").child('032677').child(str(ir['WeekendInfo']['SessionID']))\
        .child(ir['SessionInfo']['Sessions'][ir['SessionNum']]['SessionName'])\
        .child("Lap " + str(ir['Lap'] - 1).zfill(3)).set(SFdata)





def checkifpitting(state, ir):
    if ir['CarIdxTrackSurface'][state.idx] == 2 and state.pitting == False:
        state.sleeptime = 0.1
        state.pitting = True
        print("pitting = true")






    elif state.pitting:
        # print(ir['CarIdxTrackSurface'][state.idx])
        if ir['CarIdxTrackSurface'][state.idx] == 3:
            state.sleeptime = 0.5
            state.pitting = False
            print("pitting = false")
        elif state.inPitBox:
            if ir['CarIdxTrackSurface'][state.idx] == 2:
                state.inPitBox = False
                state.pitCounter = state.pitCounter + 1
                print("inpitbox = false")
                state.pitBoxTime = time.time() - state.pitBoxStartTime
                print(state.pitBoxTime)

        elif state.onPitRoad:
            if ir['CarIdxTrackSurface'][state.idx] == 1:
                state.pitBoxStartTime = time.time()
                state.inPitBox = True
                print("inpitbox = true")
            elif ir['OnPitRoad'] == False:
                state.pitLaneTime = time.time() - state.pitLaneStartTime
                state.onPitRoad = False
                print("onpitroad = false")
                print(state.pitLaneTime)
                state.pitUpdated = True
        elif ir['OnPitRoad']:
            state.pitLaneStartTime = time.time()
            state.onPitRoad = True
            print("onpitroad = true")





    else:
        # print(ir['SessionNum'])
        pass
            # idx = ir['DriverInfo']['DriverCarIdx']
            # print(ir['OnPitRoad'])
            # print(ir['CarIdxTrackSurface'][idx])


