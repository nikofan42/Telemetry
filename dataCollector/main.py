import irsdk
from dataCollector import DataCollector
import time

def check_iracing_connection(ir):
    if not ir.is_initialized or not ir.is_connected:
        print("Initializing iRacing SDK connection...")
        ir.startup()
        if ir.is_initialized and ir.is_connected:
            print("Connected to iRacing.")
            return True
        else:
            print("Failed to connect to iRacing.")
            return False
    else:
        print("Already connected to iRacing.")
        return True

if __name__ == '__main__':
    ir = irsdk.IRSDK()
    collector = DataCollector(ir)  # Pass ir object to DataCollector

    if check_iracing_connection(ir):
        time.sleep(2)  # Wait a few seconds to ensure the data stream is ready
        collector.run()  # Run the data collection loop
    else:
        print("Cannot collect data without iRacing connection.")
