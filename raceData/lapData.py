import json
import os
import ijson
def generate_lap_summaries(car_idx):
    lap_summaries = {}
    with open('raceData/telemetry_data.json', 'rb') as file:  # Open in binary mode
        for data_entry in ijson.items(file, 'item'):
            if "CarIdxTelemetry" in data_entry and car_idx in data_entry["CarIdxTelemetry"]:
                car_data = data_entry["CarIdxTelemetry"][car_idx]
                lap = car_data.get("Lap")
                if lap and lap not in lap_summaries:
                    lap_summaries[lap] = {
                        "Lap": lap,
                        "ClassPosition": car_data.get("ClassPosition"),
                        "EstTime": car_data.get("EstTime"),
                        "F2Time": car_data.get("F2Time"),
                        "LapDistPct": car_data.get("LapDistPct"),
                        "Position": car_data.get("Position"),
                        "RPM": car_data.get("RPM"),
                        "Steer": car_data.get("Steer"),
                        "TrackSurface": car_data.get("TrackSurface"),
                        # Add other relevant data points here
                    }
    return lap_summaries

def main():
    try:
        lap_summaries = generate_lap_summaries(2)  # Car index 2
        with open('lap_summaries.json', 'w') as outfile:
            json.dump(lap_summaries, outfile, indent=4)
            print("Lap summaries saved to lap_summaries.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

