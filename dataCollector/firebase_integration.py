import firebase_admin
from firebase_admin import credentials, db

class FirebaseIntegration:
    def __init__(self):
        # Initialize the Firebase Admin SDK
        self.cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://your-database-url.firebaseio.com'
        })

    def send_data(self, data, path='your_data_path'):
        print("Trying to send data...")
        ref = db.reference(path)
        ref.push(data)
        print("Data sent to Firebase.")
