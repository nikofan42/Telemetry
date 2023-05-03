import irsdk

class PyirsdkWrapper(irsdk.IRSDK):
    def __init__(self, recorded_data=None):
        self.recorded_data_generator = (data for data in recorded_data) if recorded_data else None
        self.use_recorded_data = bool(recorded_data)
        super().__init__()

    def get_telemetry(self):
        if self.use_recorded_data:
            try:
                return next(self.recorded_data_generator)
            except StopIteration:
                print("End of recorded data.")
                return None
        else:
            self.update_data()
            return {key: self[key] for key in self.keys()}

    def get_value(self, key):
        telemetry_data = self.get_telemetry()
        if telemetry_data is not None and key in telemetry_data:
            return telemetry_data[key]
        else:
            return None

def initialize_irsdk(recorded_data=None):
    return PyirsdkWrapper(recorded_data)
