#AJA TÄMÄ FILE


#from backend import *
import pyrebase
import time
from backend import *



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



i = 0


while True: # tätä loopataan maailman loppuun asti
    x = db.child("Backend Ingest").get()
    print(x.each())
    if x.each() == None: # Onko Backend Ingest -kansio tyhjä

        time.sleep(10) #mene nukkumaan jos on, aika on sekunneissa
        print("it is empty yes")
    else:
        for item in x.each():
            processIngest(item.key()) #
        time.sleep(20) #20 sekkaa lepoa kun on hoitanut koko Backend Ingest Kansion.

    i = i + 1

