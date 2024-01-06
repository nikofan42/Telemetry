import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import time

#cred = credentials.Certificate("../auth.json")
#firebase_admin.initialize_app(cred, {'databaseURL': 'https://iracingai-default-rtdb.europe-west1.firebasedatabase.app'})
#db = firebase_db.reference()

#ingest -> poista
#

#config = {
#    "apiKey": "AIzaSyB5-lkeChuEgkJ0UXYbf6WUP33fIBNYVdA",
#    "authDomain": "iracingai.firebaseapp.com",
#    "databaseURL": "https://iracingai-default-rtdb.europe-west1.firebasedatabase.app",
#    "projectId": "iracingai",
#    "databaseURL": "https://iracingai-default-rtdb.europe-west1.firebasedatabase.app/",
#    "storageBucket": "iracingai.appspot.com",
#    "messagingSenderId": "536602400542",
#    "appId": "1:536602400542:web:17ef9c0bedfcf074209b0f",
#    "measurementId": "G-CDHEMNLTZT"
#};


#firebase = pyrebase.initialize_app(config)
#db = firebase.database()


def processIngest(appID, db):


    sessions = ["TESTING", "PRACTICE", "RACE", "QUALIFYING"]
    c = db.child("Backend").child("Backend Ingest").child(appID).get()
    print(type(c))
    sessionIDs = c.keys()
    #print(sessionIDs)

    for sessionID in sessionIDs:
        print("and this")
        print(type(sessionID))#käy joka sessio yks kerrallaan
        sessionID = str(sessionID)
        print(type(sessionID))
        d = db.child("Backend").child("Backend Ingest").child(appID).child(str(sessionID)).get()
        for session in d.keys():
            #print("this")
            #print(type(sessionID))
            #print(sessionID)
            data = db.child("Backend").child("Backend Ingest").child(appID).child(str(sessionID)).child(session).get()
            #elikkä ekana backend ingest/appID(jaakon id)/sessionID(iracingin id)/PRACTICE, jne
            try:



    ##############################Tän alla pitäisi kaikki toimia#######################################################################
                counter = 0


                #tässä on vaan dataa:
                for item in data.keys():
                    datadict = db.child("Backend").child("Backend Ingest").child(appID).child(str(sessionID)).child(session).child(item).get()

                    print("datadict is")
                    print("appid is")
                    print(appID)
                    print("sessionId is")
                    print(sessionID)
                    print("session is")
                    print(session)
                    print("item is")
                    print(item)
                    print(datadict)
                    counter = counter + 1
                    #data = item.val()
                    #b = item.key()
                    #print(b)
                    lap = str(int(item[3:]))
                    #print(item)
                    #print(lap)
                    #lap = str(int(b))
                    airtemp = datadict['Air temperature']
                    fuellvl = datadict['Fuel Level']
                    fuelusedlastlap = datadict['Fuel used']
                    #lapscomplete = data['Laps complete']
                    lapscomplete = item[-3:]
                    laptime = datadict['Laptime']
                    cumulativeincident = datadict['Player car incident amount']
                    position = datadict['Position']
                    racelapscomplete = datadict['Race laps complete']
                    sessiontimeelapsed = datadict['Session time elapsed']
                    sessiontimeremaining = datadict['Session time remaining']
                    winddirection = datadict['Wind direction']
                    windvelocity = datadict['Wind velocity']
                    fueltanksize = datadict['Fuel tank size']
                    sessionName = datadict["Session name"]
                    #sessionID = datadict["SessionID"]
                    gap2Leader = datadict["Gap to leader"]
                    name = datadict['My name is']
                    timestamp = datadict["Timestamp"]
                    trackState = datadict["Session track state"]
                    pittedLastLap = datadict['Pitted last lap']
                    pitBoxTime = datadict['Pitbox time']
                    pitLaneTime = datadict['Pitlane time']
                    #fueltanksize = data['Fuel tank size']
                    if counter == 0:
                        fuelusedlastlap = "1.0"

                    if float(fuelusedlastlap == "0.0"):
                        fuelusedlastlap = "0.1"


                    stintlapsremaining = round(float(fuellvl) / float(fuelusedlastlap))


                    laptimefloat = float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100


                    stinttimeremaining = round(int(stintlapsremaining) * (float(laptime[0:2])*60 + float(laptime[3:5]) + float(laptime[6:])/100))


                    indices = []
                    for i in range(len(sessiontimeremaining)):
                        if sessiontimeremaining[i] == ":":
                            indices.append(i)


                    try: #yritä laskea nämä muuttujat, mene except-kohtaan jos kierros aika/bensan kulutus on 0
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


                    db.child("Backend").child("Backend output").child(appID).child(str(sessionID)).child(sessionName).child("Laps").child("Lap " + lapscomplete).set(data)
                    #db.child("Backend output").child(appID).child(sessionID).child(sessionName).set(data)

                    raceVariables = {       #Jaakon käyttämät muuttujat ovat tässä alla
                        "Position": position,
                        "Gap to leader(s)": gap2Leader,
                        "Incident amount": cumulativeincident,
                        "Final stint lap count": finalstintlaps,
                        "Stint time remaining(s)": stinttimeremaining,
                        "Last lap time":laptime,
                        "Lap:": str(int(lapscomplete) + 1)
                    };
                    print(laptime)

                    db.child("Backend").child("Backend output").child(appID).child(str(sessionID)).child(sessionName).child("Race Variables").update(raceVariables)
                    #try:
                    #    db.child("Backend").child("Backend output").child(appID).child(str(sessionID)).child(
                    #        sessionName).child("Race Variables").delete()
                    #    time.sleep(10)
                    #except Exception as e: print(e)

                    #db.child("Backend").child("Backend output").child(appID).child(str(sessionID)).child(
                    #    sessionName).child("Race Variables").set(raceVariables)
                        #"Current traffic value": tra,
                        #"My name is": str(state.myName)
                    db.child("Backend").child("Backend Ingest").child(appID).child(str(sessionID)).child(session).child(item).delete()

            except NameError:
                print("something wrong with data")




