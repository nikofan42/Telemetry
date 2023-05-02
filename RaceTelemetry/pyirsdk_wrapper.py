import pyirsdk

class PyirsdkWrapper(pyirsdk.IRSDK):
    def __init__(self, recorded_data):
        self.recorded_data_generator = (data for data in recorded_data)
        super().__init__()

    def get_telemetry(self):
        try:
            return next(self.recorded_data_generator)
        except StopIteration:
            print("End of recorded data.")
            return None

    def __getitem__(self, key):
        telemetry_data = self.get_telemetry()
        if telemetry_data is not None and key in telemetry_data:
            return telemetry_data[key]
        else:
            return super().__getitem__(key)
