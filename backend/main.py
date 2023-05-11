import pyrebase
import time



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
data = {"a1":3}
db.child("Backend Ingest").update(data)
print("this")
x = db.child("Backend Ingest").get()
for item in x.each():
    print(item.key())
print(x.each())
print("is")

while True and i < 10:
    x = db.child("Backend Ingest").get()
    print(x.each())
    if x.each() == None:

        time.sleep(1)
        print("it is empty yes")
    else:
        pass

    i = i + 1

for item in x.each():
    print(item.key())