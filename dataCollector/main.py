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
    collector = DataCollector()

    if check_iracing_connection(ir):
        last_session_info_time = time.time()

        while ir.is_initialized and ir.is_connected:
            print("Gathering data...", end='\r')  # Overwrites the same line with each print
            current_time = time.time()

            # Collect high-frequency data
            collector.collect_high_frequency_data(ir)

            # Collect SessionInfo every minute
            if current_time - last_session_info_time >= 60:
                collector.collect_session_info(ir)
                last_session_info_time = current_time

            time.sleep(0.1)  # Collect high-frequency data 10 times per second

        collector.save_data_stream()
    else:
        print("Cannot collect data without iRacing connection.")

