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


def processIngest(appID):


    sessions = ["PRACTICE", "RACE", "QUALIFYING"]
    c = db.child("Backend Ingest").child(appID)
    sessionID = c.each().key()

    for session in sessions:                        #käy joka sessio yks kerrallaan
        data = db.child("Backend Ingest").child(appID).child(sessionID).child(session)
        #elikkä ekana backend ingest/appID(jaakon id)/sessionID(iracingin id)/PRACTICE, jne
        if data.each() == None:                     #onko siellä folderissa mitään
            print("no data in folder: " + session)
        else:

##############################Tän alla pitäisi kaikki toimia#######################################################################
            counter = 0


            #tässä on vaan dataa:
            for item in data.each():
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
                print(lapscomplete)
                db.child("Backend output").child(appID).child(sessionID).child(sessionName).child("Laps").child("Lap " + lapscomplete).set(data)
                raceVariables = {       #Jaakon käyttämät muuttujat ovat tässä alla
                    "Position": position,
                    "Gap to leader(s)": gap2Leader,
                    "Incident amount": cumulativeincident,
                    "Final stint lap count": finalstintlaps,
                    "Stint time remaining(s)": stinttimeremaining
                };

                db.child("Backend output").child(appID).child(sessionID).child(sessionName).child("Race Variables").update(raceVariables)
                    #"Current traffic value": tra,
                    #"My name is": str(state.myName)




