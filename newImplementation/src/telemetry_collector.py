from typing import Optional, Dict, Any
import time
import logging
from dataclasses import dataclass
from .iracing_client import IRacingClient
from .firebase_client import FirebaseClient, FirebaseConfig

@dataclass
class CollectorConfig:
    """Configuration for the telemetry collector."""
    firebase_config: FirebaseConfig
    update_rate: float = 1/60  # 60Hz default
    weather_update_rate: float = 1/10  # 10Hz for weather
    batch_size: int = 100

class TelemetryCollector:
    """Main class for collecting and storing iRacing telemetry data."""
    
    def __init__(self, config: CollectorConfig):
        self._config = config
        self._ir_client = IRacingClient()
        self._fb_client = FirebaseClient(config.firebase_config)
        self._running = False
        self._last_weather_update = 0
        self._current_car_idx = -1
        self._last_lap_numbers: Dict[int, int] = {}
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self._logger = logging.getLogger(__name__)

    def start(self) -> bool:
        """Start collecting telemetry data."""
        if not self._ir_client.connect():
            self._logger.error("Failed to connect to iRacing")
            return False
            
        self._running = True
        self._fb_client.start_new_session()
        self._logger.info("Started new telemetry collection session")
        return True

    def stop(self):
        """Stop collecting telemetry data."""
        self._running = False
        self._fb_client.end_session()
        self._ir_client.disconnect()
        self._logger.info("Ended telemetry collection session")

    def _should_update_weather(self) -> bool:
        """Check if weather data should be updated."""
        current_time = time.time()
        if current_time - self._last_weather_update >= (1 / self._config.weather_update_rate):
            self._last_weather_update = current_time
            return True
        return False

    def _process_lap_completion(self, car_idx: int, current_lap: int):
        """Process lap completion for a car."""
        if car_idx not in self._last_lap_numbers:
            self._last_lap_numbers[car_idx] = current_lap
            return
            
        if current_lap > self._last_lap_numbers[car_idx]:
            # Lap completed, store lap data
            telemetry = self._ir_client.get_car_telemetry(car_idx)
            if telemetry:
                self._fb_client.store_lap_data(
                    car_idx,
                    self._last_lap_numbers[car_idx],
                    telemetry
                )
            self._last_lap_numbers[car_idx] = current_lap

    def collect_data(self):
        """Main data collection loop."""
        if not self._running or not self._ir_client.is_connected():
            return
            
        # Update session state
        session_state = self._ir_client.get_session_state()
        if session_state:
            self._fb_client.update_session_state(session_state)
            
        # Update weather data at lower frequency
        if self._should_update_weather():
            weather_data = self._ir_client.get_weather_data()
            if weather_data:
                self._fb_client.store_weather(weather_data)
                
        # Get telemetry for current car
        if self._current_car_idx >= 0:
            telemetry = self._ir_client.get_car_telemetry(self._current_car_idx)
            if telemetry:
                self._fb_client.store_telemetry(self._current_car_idx, telemetry)
                # Check for lap completion
                current_lap = telemetry['position']['lap']
                self._process_lap_completion(self._current_car_idx, current_lap)
                
        # Wait for next update
        self._ir_client.wait_for_update()

    def set_current_car(self, car_idx: int):
        """Set the current car to collect detailed telemetry for."""
        self._current_car_idx = car_idx
        self._logger.info(f"Now collecting detailed telemetry for car {car_idx}")

    def run(self):
        """Run the collector until stopped."""
        try:
            if not self.start():
                return
                
            self._logger.info("Starting telemetry collection loop")
            while self._running:
                self.collect_data()
                
        except KeyboardInterrupt:
            self._logger.info("Received interrupt signal")
        except Exception as e:
            self._logger.error(f"Error in telemetry collection: {str(e)}")
        finally:
            self.stop()
            self._fb_client.cleanup() 