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

a = db.child("test").child("roadamerica full 2023-03-31 20:18:05").get()
#print(a.key())
for item in a.each():
    print(item.key(), " wow", item.val())
lst = [None] * len(a.each())
print(len(lst))