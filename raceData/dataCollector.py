import irsdk
import json
from collections import defaultdict

class DataCollector:
    def __init__(self, save_data=False, file_path='data_stream.json'):
        self.ir = irsdk.IRSDK()
        self.save_data = save_data
        self.file_path = file_path
        self.data_stream = []

    def collect_all_data(self):
        if not self.ir.is_initialized or not self.ir.is_connected:
            self.ir.startup()
        if self.ir.is_initialized and self.ir.is_connected:
            current_data = {}
            for varname in self.ir.get_session_info().keys():
                current_data[varname] = self.ir[varname]
            self.data_stream.append(current_data)

    def save_data_stream(self):
        if self.save_data and self.data_stream:
            with open(self.file_path, 'w') as file:
                json.dump(self.data_stream, file)

    def generate_data_summary(self):
        data_summary = defaultdict(int)
        for data_point in self.data_stream:
            for key in data_point.keys():
                data_summary[key] += 1
        return dict(data_summary)

# Example usage
if __name__ == '__main__':
    collector = DataCollector(save_data=True)
    collector.collect_all_data()
    collector.save_data_stream()
    summary = collector.generate_data_summary()
    print(summary)
