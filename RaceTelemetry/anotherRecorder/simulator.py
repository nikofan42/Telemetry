import csv
import ast


class CSV_IRSDK:
    def __init__(self, file_path):
        self.file_path = file_path
        self.telemetry_data = []
        self.current_index = 0

        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    try:
                        row[key] = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        pass
                self.telemetry_data.append(row)

    def __getitem__(self, key):
        return self.telemetry_data[self.current_index][key]

    def next(self):
        self.current_index += 1
