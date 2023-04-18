import pyrebase

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

#a = db.child("test").child("roadamerica full 2023-03-31 20:18:05").get()
#print(a.key())
#flag = False
#for item in a.each():
#    if flag: break#
#
#    b = item.key()
#    print(b)
#    b = str(int(b[3:])).zfill(3)#

#    print(b)
#    #db.child("nikon test").child("roadamerica full 2023-03-31 20:18:05").child("Lap " + b).push(item.val())
#    #data ={"Age": 21, "Name": "Benna", "Employed": True, "Vector": [1, 2, 3, 4]}

#    db.child("nikon test").child("roadamerica full 2023-03-31 20:18:05").child("Lap " + b).set(item.val())
    #flag = True

#lst = [None] * len(a.each())
#print(len(lst))


#a = db.child("nikon test").child("roadamerica full 2023-03-31 20:18:05").get()
a = db.child("nikon testing setit").child("0").child("TESTING").get()
counter = 0
for item in a.each():
    counter = counter + 1
    data = item.val()
    b = item.key()
    #lap = str(int(b[3:]))
    lap = str(int(b))
    airtemp = data['Air temperature']
    fuellvl = data['Fuel Level']
    fuelusedlastlap = data['Fuel used']
    lapscomplete = data['Laps complete']
    laptime = data['Laptime']
    cumulativeincident = data['Player car incident amount']
    position = data['Position']
    racelapscomplete = data['Race laps complete']
    sessiontimeelapsed = data['Session time elapsed']
    sessiontimeremaining = data['Session time remaining']
    winddirection = data['Wind direction']
    windvelocity = data['Wind velocity']
    fueltanksize = data['Fuel tank size']
    sessionName = data["Session name"]
    sessionID = data["SessionID"]
    gap2Leader = data["Gap to leader"]
    name = data['My name is']
    timestamp = data["Timestamp"]
    trackState = data["Session track state"]
    pittedLastLap = data['Pitted last lap']
    pitBoxTime = data['Pitbox time']
    pitLaneTime = data['Pitlane time']
    #fueltanksize = data['Fuel tank size']
    if counter == 0:
        fuelusedlastlap = "1.0"
    #print()
    #print("Lap " + lap)
    #print(float(fuellvl))
    #print(laptime)
    stintlapsremaining = round(float(fuellvl) / float(fuelusedlastlap),1)
    print(round(float(fuellvl)))
    print(float(fuelusedlastlap))
    print(stintlapsremaining)
    laptimefloat = float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100
    print(laptimefloat)

    stinttimeremaining = int(stintlapsremaining) * (float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100)
    print(stinttimeremaining)
        #stinttimeremaining = str(int(stinttimeremaining // 60)).zfill(2) + ":"\
        #                 + str(int(stinttimeremaining - ((stinttimeremaining // 60)*60))).zfill(2) + "."\
        #                 + str(round(stinttimeremaining-int(stinttimeremaining),4))[2:-1]
        #print(float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100)
        #print( stinttimeremaining)
        #print(stinttimeremaining - stinttimeremaining // 60)
        #print(float(fuelusedlastlap))
        #print(str(int(stinttimeremaining // 60)).zfill(2) + ":" + str(int(stinttimeremaining - stinttimeremaining // 60 * 60)).zfill(2))
    totallapsremaining = (float(sessiontimeremaining[0:2]) * 3600 + float(sessiontimeremaining[3:5]) * 60 \
                              + float(sessiontimeremaining[6:])) / (float(laptime[0:2]) * 60 + float(laptime[3:5]) \
                                                                    + float(laptime[6:]) / 100)
    stintlength = (fueltanksize / float(fuelusedlastlap))
    currentstintremaining = float(fuellvl)/fueltanksize
        #finalstintlaps = (totallapsremaining / stintlength - (fuellvl/fueltanksize) / stintlength \
        #                    -int(totallapsremaining / stintlength - (fuellvl/fueltanksize) / stintlength))
    finalstintlaps = round((totallapsremaining / stintlength - currentstintremaining \
                                - int(totallapsremaining / stintlength - currentstintremaining))*stintlength,1)

        #finalstintlaps = ((totallapsremaining / (fueltanksize / float(fuelusedlastlap)))\
        #                 - int(totallapsremaining / (fueltanksize / float(fuelusedlastlap))))\
        #                 * (fueltanksize / float(fuelusedlastlap))
        #print(finalstintlaps)
        #print("tan ylapuolella")
        #print((fueltanksize / float(fuelusedlastlap))) #stintinmitta
        #print(totallapsremaining)


    print("Bad lap time")
    totallapsremaining = "???"
    finalstintlaps = "???"
    stinttimeremaining = "???"
    #print(stintlapsremaining)
    #print(int(stintlapsremaining))

    #finalstintlaps = 0
    print(sessiontimeremaining)
    data = {
        "Fuel Level": fuellvl,
        "Fuel used": fuelusedlastlap,
        "Air temperature": airtemp,
        "Laptime": laptime,
        "Position": position,
        "Laps complete": lapscomplete,
        "Race laps complete": racelapscomplete,
        "Wind velocity": windvelocity,
        "Wind direction": winddirection,
        "Session time elapsed": sessiontimeelapsed,
        "Session time remaining": sessiontimeremaining,
        "Player car incident amount": cumulativeincident,
        "Fuel tank size": fueltanksize,
        "Session laps remaining": totallapsremaining,
        "Final stint lap count": finalstintlaps,
        "Stint time remaining": stinttimeremaining
    };
    db.child("nikon test testing test").child("testing").child("Laps").child("Lap " + lapscomplete).set(data)
    raceVariables = {
        "Position": position,
        "Gap to leader": "TODO",
        "Incident amount": cumulativeincident,
        "Final stint lap count": finalstintlaps,
        "Stint time remaining": stinttimeremaining
    };
    db.child("nikon test testing test").child("roadamerica full 2023-03-31 20:18:05").child("Race Variables").update(raceVariables)
        #"Current traffic value": tra,
        #"My name is": str(state.myName)




