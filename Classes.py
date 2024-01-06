import time

# this is our State class, with some helpful variables


class State:

    appID = ""
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
    competitorAiDataDictionary = {}
    competitorRaceDataDictionary = {}
    debug = "debug"
    sessionID = ""

class Firebase:
    db = ""
    config = ""
    firebase = ""

