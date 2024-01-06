from data_collector import DataCollector
from data_processor import DataProcessor

if __name__ == '__main__':
    collector = DataCollector(save_data=True)
    processor = DataProcessor(read_from_file=True)

    while True:
        collector.collect_data()
        collector.save_data_stream()
        processor.process_data()
        # Add any necessary sleep or loop control logic
