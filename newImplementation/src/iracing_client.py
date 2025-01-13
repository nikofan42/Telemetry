from typing import Dict, Any, Optional
import irsdk
import time
from dataclasses import dataclass
from typing_extensions import TypedDict

class SessionState(TypedDict):
    session_num: int
    session_state: int
    session_flags: int
    session_time: float
    session_time_remain: float

class WeatherData(TypedDict):
    air_density: float
    air_pressure: float
    air_temp: float
    track_temp: float
    relative_humidity: float
    fog_level: float
    skies: int
    wind_dir: float
    wind_vel: float

@dataclass
class IRacingClient:
    """Main interface for iRacing SDK data collection."""
    
    UPDATE_RATE: float = 1/60  # 60Hz default update rate
    
    def __init__(self):
        self._ir = None
        self._last_session_info = None
        self._connected = False
        self._last_car_idx = -1

    def connect(self) -> bool:
        """Establish connection to iRacing SDK."""
        if not self._ir:
            self._ir = irsdk.IRSDK()
        
        if self._ir.startup():
            self._connected = True
            return True
        return False

    def disconnect(self):
        """Disconnect from iRacing SDK."""
        if self._ir and self._connected:
            self._ir.shutdown()
            self._connected = False
            self._ir = None

    def is_connected(self) -> bool:
        """Check if connected to iRacing."""
        return self._connected and self._ir and self._ir.is_connected

    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """Get current session information."""
        if not self.is_connected():
            return None
            
        return self._ir.get_session_info()

    def get_session_state(self) -> Optional[SessionState]:
        """Get current session state."""
        if not self.is_connected():
            return None
            
        return {
            'session_num': self._ir['SessionNum'],
            'session_state': self._ir['SessionState'],
            'session_flags': self._ir['SessionFlags'],
            'session_time': self._ir['SessionTime'],
            'session_time_remain': self._ir['SessionTimeRemain']
        }

    def get_weather_data(self) -> Optional[WeatherData]:
        """Get current weather conditions."""
        if not self.is_connected():
            return None
            
        return {
            'air_density': self._ir['AirDensity'],
            'air_pressure': self._ir['AirPressure'],
            'air_temp': self._ir['AirTemp'],
            'track_temp': self._ir['TrackTemp'],
            'relative_humidity': self._ir['RelativeHumidity'],
            'fog_level': self._ir['FogLevel'],
            'skies': self._ir['Skies'],
            'wind_dir': self._ir['WindDir'],
            'wind_vel': self._ir['WindVel']
        }

    def get_car_telemetry(self, car_idx: int) -> Optional[Dict[str, Any]]:
        """Get telemetry data for a specific car."""
        if not self.is_connected():
            return None
            
        return {
            'position': {
                'lap': self._ir['Lap', car_idx],
                'lap_completed': self._ir['LapCompleted', car_idx],
                'lap_dist_pct': self._ir['LapDist', car_idx],
                'lat': self._ir['Lat', car_idx],
                'lon': self._ir['Lon', car_idx],
                'alt': self._ir['Alt', car_idx]
            },
            'timing': {
                'last_lap_time': self._ir['LapLastLapTime', car_idx],
                'best_lap_time': self._ir['LapBestLapTime', car_idx],
                'best_lap_num': self._ir['LapBestLapNum', car_idx],
                'delta_time': self._ir['LapDeltaToSessionBestLap', car_idx]
            },
            'state': {
                'gear': self._ir['Gear', car_idx],
                'rpm': self._ir['RPM', car_idx],
                'steer_angle': self._ir['SteeringWheelAngle', car_idx],
                'on_pit_road': self._ir['OnPitRoad', car_idx]
            },
            'motion': {
                'velocity': {
                    'x': self._ir['VelocityX', car_idx],
                    'y': self._ir['VelocityY', car_idx],
                    'z': self._ir['VelocityZ', car_idx]
                },
                'acceleration': {
                    'long': self._ir['LongAccel', car_idx],
                    'lat': self._ir['LatAccel', car_idx],
                    'vert': self._ir['VertAccel', car_idx]
                }
            }
        }

    def wait_for_update(self):
        """Wait for the next SDK update."""
        if self.is_connected():
            self._ir.wait_for_data(timeout=self.UPDATE_RATE) 