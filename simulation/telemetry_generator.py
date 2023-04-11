import time

#This is ourtelemetry data reader.
def telemetry_generator(telemetry_data):
    start_time = time.time()
    for data in telemetry_data:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_to_wait = data['timestamp'] - elapsed_time

        if time_to_wait > 0:
            time.sleep(time_to_wait)

        yield data