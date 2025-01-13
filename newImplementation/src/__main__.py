import argparse
import os
from dotenv import load_dotenv
from .firebase_client import FirebaseConfig
from .telemetry_collector import TelemetryCollector, CollectorConfig

def main():
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='iRacing Telemetry Collector')
    parser.add_argument(
        '--firebase-creds',
        type=str,
        default=os.getenv('FIREBASE_CREDS_PATH'),
        help='Path to Firebase credentials JSON file'
    )
    parser.add_argument(
        '--firebase-url',
        type=str,
        default=os.getenv('FIREBASE_DATABASE_URL'),
        help='Firebase database URL'
    )
    parser.add_argument(
        '--car-idx',
        type=int,
        default=int(os.getenv('DEFAULT_CAR_IDX', -1)),
        help='Car index to collect detailed telemetry for'
    )
    parser.add_argument(
        '--update-rate',
        type=float,
        default=float(os.getenv('UPDATE_RATE', '60')),
        help='Update rate in Hz'
    )
    parser.add_argument(
        '--weather-rate',
        type=float,
        default=float(os.getenv('WEATHER_UPDATE_RATE', '10')),
        help='Weather update rate in Hz'
    )
    
    args = parser.parse_args()
    
    # Validate required arguments
    if not args.firebase_creds or not args.firebase_url:
        parser.error("Firebase credentials and database URL are required. "
                    "Set them via arguments or environment variables.")
    
    # Create configuration
    firebase_config = FirebaseConfig(
        credential_path=args.firebase_creds,
        database_url=args.firebase_url
    )
    
    collector_config = CollectorConfig(
        firebase_config=firebase_config,
        update_rate=1/args.update_rate,
        weather_update_rate=1/args.weather_rate
    )
    
    # Create and run collector
    collector = TelemetryCollector(collector_config)
    if args.car_idx >= 0:
        collector.set_current_car(args.car_idx)
    
    collector.run()

if __name__ == '__main__':
    main() 