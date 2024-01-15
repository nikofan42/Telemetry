import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase(session_id, competitor_name):
    cred = credentials.Certificate('../auth.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iracingai-default-rtdb.europe-west1.firebasedatabase.app'})
    path = f'races/{session_id}/{competitor_name}'
    return db.reference(path)
