
import importlib
import pickle
import itertools
import os

import raceTelemetry
import pyirsdk_wrapper

telemetry_script = importlib.import_module('raceTelemetry')

def load_recorded_data(file_path):
    with open(file_path, 'rb') as f:
        recorded_data = pickle.load(f)
    return recorded_data

recorded_data = load_recorded_data('telemetry_data.pkl')

def receive_recorded_data():
    for data in recorded_data:
        yield data

recorded_data_generator = receive_recorded_data()

telemetry_script.receive_live_data = lambda: next(recorded_data_generator)

if hasattr(telemetry_script, 'main'):
    telemetry_script.main()
else:
    print("No main function found in the telemetry script.")
