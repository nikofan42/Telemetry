
def start(state, ir):
    state.in_startup = 0
    print(ir['DriverInfo']['DriverCarIdx'])
    state.idx = ir['DriverInfo']['DriverCarIdx']
    state.previousFuelLevel = ir['FuelLevel']

    driversData = ir['DriverInfo']['Drivers']
    driversNames = {}
    for driver in driversData:
        car_idx = driver['CarIdx']
        name = driver['UserName']
        driversNames[car_idx] = name

    state.myName = driversNames[state.idx]
    state.sessionID = ir['WeekendInfo']['SessionID']