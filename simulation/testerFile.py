# test_main.py

import time
import unittest
import asyncio
import pickle
from simulatoinTester import main
from telemetry_generator import telemetry_generator

class TestMain(unittest.TestCase):
    def test_main(self):
        # Load recorded telemetry data from the pickle file
        with open('telemetry_data.pkl', 'rb') as f:
            telemetry_data = pickle.load(f)

        # Create a generator for the telemetry data
        ir_data_generator = telemetry_generator(telemetry_data)

        # Create an async test function to call the 'process_telemetry_data' function
        async def async_test_main():
            for ir in ir_data_generator:
                print("Processing telemetry data:", ir)  # Add a print statement here
                await process_telemetry_data(ir)

        # Run the async test function
        asyncio.run(async_test_main())

        # Add any assertions to check if the script produces the expected results

if __name__ == '__main__':
    unittest.main()
