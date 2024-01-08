import json
import pandas as pd

def read_json_in_chunks(file_path, chunk_size=1024 * 1024):
    with open(file_path, 'r') as file:
        chunk = ""
        for line in file:
            chunk += line
            try:
                data = json.loads(chunk)
                print("Chunk read successfully.")  # Debugging statement
                yield data
                chunk = ""
            except json.JSONDecodeError:
                continue  # Continue accumulating the chunk until a complete JSON object is formed


def filter_car_data(data_stream, car_index):
    filtered_data = []
    for entry in data_stream:
        if 'CarIdxTelemetry' in entry and str(car_index) in entry['CarIdxTelemetry']:
            car_data = entry['CarIdxTelemetry'][str(car_index)]
            if 'Lap' in car_data and car_data['Lap'] >= 0:
                car_data['timestamp'] = entry['timestamp']
                filtered_data.append(car_data)
    print(f"Filtered data for car index {car_index}: {filtered_data[:5]}")  # Print first 5 entries for debugging
    return filtered_data



def aggregate_by_lap(car_data):
    df = pd.DataFrame(car_data)
    if df.empty or 'Lap' not in df.columns:
        print("No valid lap data found or 'Lap' column is missing in the DataFrame.")
        return None
    summary = df.groupby('Lap').agg({
        'timestamp': 'first',
        'EstTime': 'mean',
        'F2Time': 'mean',
        'Gear': 'mean',
        'LapDistPct': 'mean',
        'OnPitRoad': 'max',
        'Position': 'mean',
        'RPM': 'mean',
        'Steer': 'mean',
        'TrackSurface': 'max',
    }).reset_index()
    return summary

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main(file_path, car_index):
    data_stream = load_data(file_path)
    print(f"First data entry: {json.dumps(data_stream[0], indent=2)[:1000]}")  # Print first 1000 characters of the first entry

    car_data = filter_car_data(data_stream, car_index)
    if not car_data:
        print("No data collected for car index:", car_index)
        return

    lap_summary = aggregate_by_lap(car_data)
    if lap_summary is not None:
        print(lap_summary)
        lap_summary.to_csv('race_summary.csv', index=False)
    else:
        print("No valid lap data found or 'Lap' column is missing in the DataFrame.")

if __name__ == '__main__':
    FILE_PATH = 'dataCollector/telemetry_data.json'  # Replace with your file path
    CAR_INDEX = 13
    main(FILE_PATH, CAR_INDEX)


