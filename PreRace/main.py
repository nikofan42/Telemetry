import firebase_admin
import math
from firebase_admin import credentials
from firebase_admin import db as firebase_db
from mathTools import *


cred = credentials.Certificate("../auth.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iracingai-default-rtdb.europe-west1.firebasedatabase.app'})
db = firebase_db.reference()

def time_check(time):
    if len(time) != 8:
        raise Exception("Input driver time in minmin:secsec:hh")
    if time[2] != ":":
        print(time[3])
        raise Exception("Use :-symbol to separate minutes and seconds. minmin:secsec:hh")
    if time[5] != ".":
        raise Exception("Use .-symbol to separate minutes and hundredths. minmin:secsec:hh")
    if len(time.split(":")[0]) != 2 :
        raise Exception("Insufficient number of minutes")
    if len(time.split(".")[1]) != 2 :
        raise Exception("Insufficient number of hundredths")
    if len(time.split(".")[0].split(":")[1]) != 2:
        raise Exception("Insufficient number of seconds")



def raceVariables():
    race_name = input("Name of the race (optional)");
    race_length = input("Length of the race (hours)");
    full_tank = input("Full tank of fuel (litres)")
    maxfuelcons = input("Estimated max fuel consumption (litres)")

    minlaps = math.floor(float(full_tank)/float(maxfuelcons))

    js = {"Race name": race_name,
          "Race Length": race_length + " hours",
          "Full tank": full_tank + " litres",
          "Fuel targets": {str(int(minlaps)): str(round(float(full_tank)/(minlaps),2)),
                           str(int(minlaps) + 1): str(round(float(full_tank)/(minlaps+1.0),2)),
                           str(int(minlaps) + 2): str(round(float(full_tank)/(minlaps+2.0),2)),
                           str(int(minlaps) + 3): str(round(float(full_tank)/(minlaps+3.0),2)),
                           str(int(minlaps) + 4): str(round(float(full_tank)/(minlaps+4.0),2))}
          }


    db.child("Pre race").child("Race Info").set(js)

def pitVariables():
    stop_time = input("Length of full pit stop (seconds)")
    pit_loss = input("Pit loss (seconds) (How much time lost with full pit)")

    js = {
        "Pit stop time": stop_time,
        "Pit loss": pit_loss
    }
    db.child("Pre race").child("Pit Info").set(js)

def calculateRaceLaps():
    drivers = db.child("Pre race").child("Drivers").get()

    arr = []

    for driver in list(drivers.keys()):
        arr.append(db.child("Pre race").child("Drivers").child(driver).child("time").get())

    sum = 0
    i = 0
    for time in arr:
        sum += mintosec(time)
        i += 1

    avg = sum/i;
    avgstring = sectomin(avg)

    pit_loss = db.child("Pre race").child("Pit Info").child("Pit loss").get()
    pit_stop = db.child("Pre race").child("Pit Info").child("Pit stop time").get()


    stint_time = 29 * avg + int(pit_loss)

    laps = 24*60*60 / stint_time
    laps = round(laps * 29,2)

    print("The estimated amount of laps is " + str(laps))


def ask():
    while True:
        cmd = input()
        match cmd.split()[0]:
            case "get":
                try:
                    match cmd.split()[1]:
                        case "drivers":
                            print(db.child("Pre race").child("Drivers").get())
                        case "race":
                            print(db.child("Pre race").child("Race Info").get())
                        case "pit":
                            print(db.child("Pre race").child("Pit Info").get())
                except Exception as error:
                    # handle the exception
                    print("An exception occurred:", error)  # An exception occurred: division by zero

            case "quit":
                quit()
            case "add":
                try:
                    time = cmd.split()[2]
                    time_check(time)

                    javascript = {cmd.split()[1]: {"time": time, "laps": 1}}
                    db.child("Pre race").child("Drivers").update(javascript)
                    #db.child("Pre race").child("Drivers").set(cmd.split()[1])
                except Exception as error:
                    # handle the exception
                    print("An exception occurred:", error)  # An exception occurred: division by zero
            case "delete":
                db.child("Pre race").child("Drivers").child(cmd.split()[1]).delete()
            case "update":
                try:
                    time = cmd.split()[2]
                    time_check(time)

                    js = {cmd.split()[1]: {"time": time, "laps": 1}}
                    db.child("Pre race").child("Drivers").update(js)

                except Exception as error:
                    # handle the exception
                    print("An exception occurred:", error)  # An exception occurred: division by zero
            case "clear":
                print(db.child("Pre race").child("Drivers").delete())
            case "race":
                raceVariables()
            case "pit":
                pitVariables()
            case "calc":
                calculateRaceLaps()

if __name__ == '__main__':
    ask()
