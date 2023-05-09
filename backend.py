import pyrebase

#ingest -> poista
#

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

#x = db.child("abc").get()
#p#rint(x)
#print(sys.getsizeof(x)*100000/1000)
#for i in range(100000):
#    if x.each() == None:
#        print("hell yeah")
#for item in x.each():
#    print(item)

a = db.child("nikon testing setit").child("203948265").child("RACE").get()
print(a)
counter = 0


for item in a.each():
    print(item.key()[-3:])

for item in a.each():
    counter = counter + 1
    data = item.val()
    b = item.key()
    lap = str(int(b[3:]))
    #lap = str(int(b))
    airtemp = data['Air temperature']
    fuellvl = data['Fuel Level']
    fuelusedlastlap = data['Fuel used']
    #lapscomplete = data['Laps complete']
    lapscomplete = item.key()[-3:]
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

    if float(fuelusedlastlap == "0.0"):
        fuelusedlastlap = "0.1"
    #print()
    #print("Lap " + lap)
    #print(float(fuellvl))
    #print(laptime)
    stintlapsremaining = round(float(fuellvl) / float(fuelusedlastlap))
    #print(round(float(fuellvl)))
    #print(float(fuelusedlastlap))
    #print(stintlapsremaining)
    laptimefloat = float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100
    #print(laptimefloat)

    stinttimeremaining = round(int(stintlapsremaining) * (float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100))
    #print(stinttimeremaining)
        #stinttimeremaining = str(int(stinttimeremaining // 60)).zfill(2) + ":"\
        #                 + str(int(stinttimeremaining - ((stinttimeremaining // 60)*60))).zfill(2) + "."\
        #                 + str(round(stinttimeremaining-int(stinttimeremaining),4))[2:-1]
        #print(float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100)
        #print( stinttimeremaining)
        #print(stinttimeremaining - stinttimeremaining // 60)
        #print(float(fuelusedlastlap))
        #print(str(int(stinttimeremaining // 60)).zfill(2) + ":" + str(int(stinttimeremaining - stinttimeremaining // 60 * 60)).zfill(2))
    #print("Hi")
    #print(sessiontimeremaining)
    #print(lap)
    #print(sessiontimeremaining.rfind(":"))
    indices = []
    for i in range(len(sessiontimeremaining)):
        if sessiontimeremaining[i] == ":":
            indices.append(i)

    #for i in(indices):
    #    print(i)
    #print(min(indices))
    #print(max(indices))
    #print(sessiontimeremaining[0:min(indices)])
    #print(sessiontimeremaining[min(indices) + 1:max(indices)])
    #print(sessiontimeremaining[max(indices) + 1:])

    #print(float(laptime[0:2]) * 60 + float(laptime[3:5]) \
    #                                                                + float(laptime[6:]) / 100)

    #return [i for i, letter in enumerate(s) if letter == ch]
    try:
        totallapsremaining = round((float(sessiontimeremaining[0:min(indices)]) * 3600 + float(sessiontimeremaining[min(indices) + 1:max(indices)]) * 60 \
                              + float(sessiontimeremaining[max(indices) + 1:])) / (float(laptime[0:2]) * 60 + float(laptime[3:5]) \
                                                                    + float(laptime[6:]) / 100),1)
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

    except:
        print("Bad lap time on lap " + str(lap) + ", it is:")
        print(laptime)
        totallapsremaining = "???"
        finalstintlaps = "???"
        stinttimeremaining = "???"
    #print(stintlapsremaining)
    #print(int(stintlapsremaining))

    #finalstintlaps = 0
    data = {
        "Fuel Level(l)": fuellvl,
        "Fuel used(l)": fuelusedlastlap,
        "Air temperature(C)": airtemp,
        "Laptime": laptime,
        "Position": position,
        "Laps complete": lapscomplete,
        "Race laps complete": racelapscomplete,
        "Wind velocity(m per s)": windvelocity,
        "Wind direction(deg)": winddirection,
        "Session time elapsed": sessiontimeelapsed,
        "Session time remaining": sessiontimeremaining,
        "Player car incident amount": cumulativeincident,
        "Fuel tank size(l)": fueltanksize,
        "Session laps remaining": totallapsremaining,
        "Final stint lap count": finalstintlaps,
        "Stint time remaining(s)": stinttimeremaining,
        "Session name": sessionName,
        "Session ID": sessionID,
        "Gap to Leader": gap2Leader,
        "Name": name,
        "Timestamp": timestamp,
        "Track state": trackState,
        "Pitted last lap": pittedLastLap,
        "Pit box time": pitBoxTime,
        "Pit lane time": pitLaneTime
    };
    print(lapscomplete)
    db.child("nikon test testing test").child(sessionName).child("Laps").child("Lap " + lapscomplete).set(data)
    raceVariables = {
        "Position": position,
        "Gap to leader(s)": gap2Leader,
        "Incident amount": cumulativeincident,
        "Final stint lap count": finalstintlaps,
        "Stint time remaining(s)": stinttimeremaining
    };
    db.child("nikon test testing test").child(sessionName).child("Race Variables").update(raceVariables)
        #"Current traffic value": tra,
        #"My name is": str(state.myName)




