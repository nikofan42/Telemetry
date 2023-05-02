import importlib
import pickle
import itertools
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pyirsdk_wrapper
import raceTelemetry

telemetry_script = importlib.import_module('raceTelemetry')

def load_recorded_data(file_path):
    with open(file_path, 'rb') as f:
        recorded_data = pickle.load(f)
    return recorded_data

recorded_data = load_recorded_data(os.path.join(project_root, 'telemetry_data.pkl'))

telemetry_script.irsdk = pyirsdk_wrapper.PyirsdkWrapper(recorded_data)

if hasattr(telemetry_script, 'main'):
    telemetry_script.main()
else:
    print("No main function found in the telemetry script.")
