import json
from firebase_integration import FirebaseIntegration

class DataProcessor:
    def __init__(self, read_from_file=False, file_path='data_stream.json'):
        self.read_from_file = read_from_file
        self.file_path = file_path
        self.firebase = FirebaseIntegration()

    def process_data(self):
        data_stream = []
        if self.read_from_file:
            with open(self.file_path, 'r') as file:
                data_stream = json.load(file)
        # Process data stream
        for data in data_stream:
            # Extract and process necessary data
            processed_data = self.extract_and_process_data(data)
            # Send to Firebase
            self.firebase.send_data(processed_data)

    def extract_and_process_data(self, data):
        # Extract and process the required data from the dataset
        # Example: processed_data = {'SessionInfo': data['SessionInfo']}
        # Return the processed data
        return processed_data
