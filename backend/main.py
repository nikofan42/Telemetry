#AJA TÄMÄ FILE


#from backend import *
#import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import time
from backend import *



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

cred = credentials.Certificate("../auth.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iracingai-default-rtdb.europe-west1.firebasedatabase.app'})
db = firebase_db.reference()



i = 0
#pip3 install -r .\requirements.txt

while True: # tätä loopataan maailman loppuun asti
    x = db.child("Backend").child("Backend Ingest").get()

    try:
        for item in x.keys():
            print(item)
            processIngest(item, db) #
        time.sleep(1) #20 sekkaa lepoa kun on hoitanut koko Backend Ingest Kansion.

    except NameError:
        print("it is empty")
        time.sleep(3)
    except AttributeError:
        print("it does not exist")
        time.sleep(3)



    #print(x.each())


