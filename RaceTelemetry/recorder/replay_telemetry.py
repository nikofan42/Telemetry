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
            return None

    def startup(self, *args, **kwargs):
        if not self.use_recorded_data:
            super().startup(*args, **kwargs)

    def __getitem__(self, key):
        if self.use_recorded_data:
            telemetry_data = self.get_telemetry()
            if telemetry_data is not None and key in telemetry_data:
                return telemetry_data[key]

        if not self.use_recorded_data:
            # Ensure data is updated before accessing live data
            if not self.is_initialized:
                self.startup()
            if not self.is_connected:
                self.shutdown()
                self.startup()

            return super().__getitem__(key)
        else:
            raise KeyError(f"Key '{key}' not found in recorded data.")

def initialize_irsdk(recorded_data=None):
    return PyirsdkWrapper(recorded_data)
