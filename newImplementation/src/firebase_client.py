import firebase_admin
from firebase_admin import credentials, firestore, db
from typing import Dict, Any, Optional, List
import time
from dataclasses import dataclass
from collections import deque
import json

@dataclass
class TeamConfig:
    """Team configuration for endurance racing."""
    team_id: str
    name: str
    car_idx: int  # Single car index
    drivers: List[str]  # List of driver IDs

@dataclass
class FirebaseConfig:
    """Firebase configuration settings."""
    credential_path: str
    database_url: str
    collection_prefix: str = "iracing"
    teams: List[TeamConfig] = None  # Team configurations

class FirebaseClient:
    """Handles all Firebase interactions for storing iRacing data."""
    
    def __init__(self, config: FirebaseConfig):
        self._config = config
        self._cred = credentials.Certificate(config.credential_path)
        self._app = firebase_admin.initialize_app(self._cred, {
            'databaseURL': config.database_url
        })
        self._db = firestore.client()
        self._rtdb = db.reference()
        self._current_session_id = None
        self._batch = self._db.batch()
        self._batch_count = 0
        self._MAX_BATCH_SIZE = 500
        self._current_drivers = {}  # Track current driver for each car
        
        # Initialize team tracking
        self._teams = {team.team_id: team for team in config.teams} if config.teams else {}
        self._car_to_team = {}
        if config.teams:
            for team in config.teams:
                self._car_to_team[team.car_idx] = team.team_id

    def _cleanup_old_data(self, car_idx: int, current_time: float):
        """Remove data points older than the window size."""
        if car_idx not in self._history_timestamps:
            self._history_timestamps[car_idx] = deque()
            return

        cutoff_time = current_time - self._window_size
        timestamps = self._history_timestamps[car_idx]
        
        while timestamps and timestamps[0] < cutoff_time:
            old_timestamp = timestamps.popleft()
            # Remove old data point from Realtime DB
            self._rtdb.child(
                f"{self._config.collection_prefix}/telemetry/{self._current_session_id}"
                f"/cars/{car_idx}/history/timestamps/{old_timestamp}"
            ).delete()

    def start_new_session(self) -> str:
        """Start a new racing session in Firebase."""
        session_ref = self._db.collection(f"{self._config.collection_prefix}/sessions").document()
        self._current_session_id = session_ref.id
        
        # Initialize session data
        session_data = {
            'start_time': firestore.SERVER_TIMESTAMP,
            'status': 'active',
            'type': 'endurance_race',
            'teams': {
                team_id: {
                    'name': team.name,
                    'car_idx': team.car_idx,
                    'drivers': team.drivers,
                    'current_driver': None,
                    'completed_stints': 0,
                    'total_laps': 0
                } for team_id, team in self._teams.items()
            }
        }
        
        session_ref.set(session_data)
        
        # Initialize team data structures in RTDB
        for team_id, team in self._teams.items():
            team_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}"
            self._rtdb.child(team_ref).set({
                'car_idx': team.car_idx,
                'current_driver': None,
                'last_pit_stop': None,
                'stint_start': None,
                'strategy': {
                    'next_driver': None,
                    'estimated_pit_window': None,
                    'fuel_remaining': None,
                    'estimated_laps_remaining': None,
                    'tire_age': None
                },
                'race_stats': {
                    'position': None,
                    'gap_to_leader': None,
                    'last_lap': None,
                    'best_lap': None,
                    'avg_lap': None,
                    'completed_laps': 0
                }
            })
        
        return self._current_session_id

    def update_session_state(self, state_data: Dict[str, Any]):
        """Update current session state."""
        if not self._current_session_id:
            return
            
        ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/state"
        self._rtdb.child(ref).update(state_data)

    def update_driver_info(self, car_idx: int, driver_info: Dict[str, Any]):
        """Update driver information for a car."""
        if not self._current_session_id:
            return
            
        # Store in realtime DB for current state
        ref = f"{self._config.collection_prefix}/telemetry/{self._current_session_id}/cars/{car_idx}/driver"
        self._rtdb.child(ref).update(driver_info)
        
        # Store in Firestore for historical record
        driver_id = driver_info.get('driver_id')
        if driver_id and driver_id != self._current_drivers.get(car_idx):
            # Driver change detected
            stint_data = {
                'car_idx': car_idx,
                'driver_id': driver_id,
                'driver_name': driver_info.get('driver_name'),
                'start_time': firestore.SERVER_TIMESTAMP,
                'status': 'active'
            }
            
            # End previous stint if exists
            if car_idx in self._current_drivers:
                self._end_driver_stint(car_idx)
            
            # Start new stint
            stint_ref = self._db.collection(
                f"{self._config.collection_prefix}/sessions/{self._current_session_id}/stints"
            ).document()
            stint_ref.set(stint_data)
            
            # Update current driver tracking
            self._current_drivers[car_idx] = driver_id

    def _end_driver_stint(self, car_idx: int):
        """End the current stint for a car."""
        if car_idx not in self._current_drivers:
            return
            
        # Find and update the active stint
        stints_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/stints"
        )
        active_stint = stints_ref.where('car_idx', '==', car_idx).where('status', '==', 'active').limit(1)
        
        for stint in active_stint.stream():
            stint.reference.update({
                'end_time': firestore.SERVER_TIMESTAMP,
                'status': 'completed'
            })

    def store_telemetry(self, car_idx: int, telemetry_data: Dict[str, Any]):
        """Store car telemetry data with historical tracking.
        Stores detailed data for team car, basic data for other cars."""
        if not self._current_session_id:
            return
            
        current_time = time.time()
        timestamp_str = str(int(current_time * 1000))
        team_id = self._car_to_team.get(car_idx)
        is_team_car = team_id is not None  # This is our team's car
        
        # Enhance telemetry data with driver information
        if car_idx in self._current_drivers:
            telemetry_data['driver_id'] = self._current_drivers[car_idx]

        if is_team_car:
            # Detailed telemetry for team car
            detailed_data = {
                'basic': {
                    'position': telemetry_data.get('position', {}),
                    'timing': telemetry_data.get('timing', {}),
                    'state': telemetry_data.get('state', {})
                },
                'detailed': {
                    'motion': telemetry_data.get('motion', {}),
                    'car_state': {
                        'fuel_level': telemetry_data.get('car_state', {}).get('fuel_level'),
                        'engine_rpm': telemetry_data.get('car_state', {}).get('engine_rpm'),
                        'engine_water_temp': telemetry_data.get('car_state', {}).get('engine_water_temp'),
                        'engine_oil_temp': telemetry_data.get('car_state', {}).get('engine_oil_temp'),
                        'brake_temp_fl': telemetry_data.get('car_state', {}).get('brake_temp_fl'),
                        'brake_temp_fr': telemetry_data.get('car_state', {}).get('brake_temp_fr'),
                        'brake_temp_rl': telemetry_data.get('car_state', {}).get('brake_temp_rl'),
                        'brake_temp_rr': telemetry_data.get('car_state', {}).get('brake_temp_rr'),
                        'tire_temp_fl': telemetry_data.get('car_state', {}).get('tire_temp_fl'),
                        'tire_temp_fr': telemetry_data.get('car_state', {}).get('tire_temp_fr'),
                        'tire_temp_rl': telemetry_data.get('car_state', {}).get('tire_temp_rl'),
                        'tire_temp_rr': telemetry_data.get('car_state', {}).get('tire_temp_rr'),
                        'tire_pressure_fl': telemetry_data.get('car_state', {}).get('tire_pressure_fl'),
                        'tire_pressure_fr': telemetry_data.get('car_state', {}).get('tire_pressure_fr'),
                        'tire_pressure_rl': telemetry_data.get('car_state', {}).get('tire_pressure_rl'),
                        'tire_pressure_rr': telemetry_data.get('car_state', {}).get('tire_pressure_rr')
                    },
                    'inputs': {
                        'throttle': telemetry_data.get('inputs', {}).get('throttle'),
                        'brake': telemetry_data.get('inputs', {}).get('brake'),
                        'clutch': telemetry_data.get('inputs', {}).get('clutch'),
                        'steering': telemetry_data.get('inputs', {}).get('steering'),
                        'gear': telemetry_data.get('inputs', {}).get('gear')
                    }
                },
                'analysis': {
                    'current_sector': telemetry_data.get('analysis', {}).get('current_sector'),
                    'sector_times': telemetry_data.get('analysis', {}).get('sector_times', {}),
                    'predicted_lap_time': telemetry_data.get('analysis', {}).get('predicted_lap_time'),
                    'tire_wear': telemetry_data.get('analysis', {}).get('tire_wear', {}),
                    'fuel_usage': telemetry_data.get('analysis', {}).get('fuel_usage', {})
                }
            }
            
            # Store current detailed state for team car
            team_car_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/car_data"
            self._rtdb.child(team_car_ref).update({
                'current': detailed_data,
                'timestamp': timestamp_str
            })
            
            # Store historical data points for analysis
            history_ref = f"{team_car_ref}/history/timestamps/{timestamp_str}"
            self._rtdb.child(history_ref).set(detailed_data)
            
            # Store in Firestore for permanent record
            self._store_historical_telemetry(car_idx, detailed_data)
            
            # Update team status with derived metrics
            self.update_team_status(car_idx, {
                'fuel_remaining': detailed_data['detailed']['car_state']['fuel_level'],
                'last_sector_time': detailed_data['analysis']['sector_times'].get('last', None),
                'predicted_lap': detailed_data['analysis']['predicted_lap_time'],
                'tire_health': detailed_data['analysis']['tire_wear']
            })
            
        else:
            # Basic telemetry for other cars
            basic_data = {
                'position': telemetry_data.get('position', {}),
                'timing': telemetry_data.get('timing', {}),
                'state': {
                    'gear': telemetry_data.get('state', {}).get('gear'),
                    'speed': telemetry_data.get('state', {}).get('speed'),
                    'on_pit_road': telemetry_data.get('state', {}).get('on_pit_road')
                }
            }
            
            # Store only basic data for other cars
            other_car_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/other_cars/{car_idx}"
            self._rtdb.child(other_car_ref).update({
                'current': basic_data,
                'timestamp': timestamp_str
            })
        
        # Process lap data if available
        if 'position' in telemetry_data and 'lap' in telemetry_data['position']:
            current_lap = telemetry_data['position']['lap']
            if is_team_car:
                self._store_detailed_lap_data(car_idx, current_lap, telemetry_data, timestamp_str)
            else:
                self._store_basic_lap_data(car_idx, current_lap, telemetry_data, timestamp_str)

    def _store_detailed_lap_data(self, car_idx: int, lap_number: int, telemetry_data: Dict[str, Any], timestamp_str: str):
        """Store detailed lap data for team car."""
        team_id = self._car_to_team[car_idx]
        lap_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/laps/{lap_number}"
        
        lap_data = {
            'timing': telemetry_data.get('timing', {}),
            'driver_id': self._current_drivers.get(car_idx),
            'timestamp': timestamp_str,
            'sectors': telemetry_data.get('analysis', {}).get('sector_times', {}),
            'fuel_used': telemetry_data.get('analysis', {}).get('fuel_usage', {}),
            'tire_wear': telemetry_data.get('analysis', {}).get('tire_wear', {}),
            'weather': self._rtdb.child(
                f"{self._config.collection_prefix}/sessions/{self._current_session_id}/weather"
            ).get()
        }
        
        self._rtdb.child(lap_ref).update(lap_data)
        
        # Store in Firestore for historical record
        doc_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/lap_history"
        ).document(f"lap_{lap_number}")
        
        self._batch.set(doc_ref, {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'lap_number': lap_number,
            'driver_id': self._current_drivers.get(car_idx),
            'data': lap_data
        })
        
        self._batch_count += 1
        if self._batch_count >= self._MAX_BATCH_SIZE:
            self.commit_batch()

    def _store_basic_lap_data(self, car_idx: int, lap_number: int, telemetry_data: Dict[str, Any], timestamp_str: str):
        """Store basic lap data for other cars."""
        lap_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/other_cars/{car_idx}/laps/{lap_number}"
        
        lap_data = {
            'lap_time': telemetry_data.get('timing', {}).get('last_lap_time'),
            'position': telemetry_data.get('position', {}).get('position'),
            'timestamp': timestamp_str
        }
        
        self._rtdb.child(lap_ref).update(lap_data)

    def _store_historical_telemetry(self, car_idx: int, telemetry_data: Dict[str, Any]):
        """Store complete telemetry data in Firestore."""
        doc_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/telemetry"
        ).document()
        
        self._batch.set(doc_ref, {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'car_idx': car_idx,
            'driver_id': self._current_drivers.get(car_idx),
            'data': telemetry_data
        })
        
        self._batch_count += 1
        if self._batch_count >= self._MAX_BATCH_SIZE:
            self.commit_batch()

    def store_weather(self, weather_data: Dict[str, Any]):
        """Store weather data."""
        if not self._current_session_id:
            return
            
        ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/weather"
        self._rtdb.child(ref).update(weather_data)

    def store_lap_data(self, car_idx: int, lap_number: int, lap_data: Dict[str, Any]):
        """Store completed lap data."""
        if not self._current_session_id:
            return
            
        doc_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/laps"
        ).document(f"car_{car_idx}_lap_{lap_number}")
        
        self._batch.set(doc_ref, {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'car_idx': car_idx,
            'lap_number': lap_number,
            'data': lap_data
        })
        
        self._batch_count += 1
        if self._batch_count >= self._MAX_BATCH_SIZE:
            self.commit_batch()

    def commit_batch(self):
        """Commit the current batch of writes."""
        if self._batch_count > 0:
            self._batch.commit()
            self._batch = self._db.batch()
            self._batch_count = 0

    def end_session(self):
        """End the current session."""
        if not self._current_session_id:
            return
            
        # Commit any remaining batched writes
        self.commit_batch()
        
        # Update session status
        session_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions"
        ).document(self._current_session_id)
        
        session_ref.update({
            'end_time': firestore.SERVER_TIMESTAMP,
            'status': 'completed'
        })
        
        self._current_session_id = None

    def cleanup(self):
        """Cleanup Firebase resources."""
        if self._current_session_id:
            self.end_session()
        firebase_admin.delete_app(self._app) 

    def store_race_stats(self, stats_data: Dict[str, Any]):
        """Store race statistics for analysis."""
        if not self._current_session_id:
            return
            
        ref = f"{self._config.collection_prefix}/telemetry/{self._current_session_id}/race_stats"
        self._rtdb.child(ref).update(stats_data)

    def get_rolling_window_data(self, car_idx: int) -> Optional[Dict[str, Any]]:
        """Get all data points in the current rolling window for a car."""
        if not self._current_session_id:
            return None
            
        ref = (f"{self._config.collection_prefix}/telemetry/{self._current_session_id}"
               f"/cars/{car_idx}/history/timestamps")
        return self._rtdb.child(ref).get()

    def get_lap_history(self, car_idx: int) -> Optional[Dict[str, Any]]:
        """Get lap history data for a car."""
        if not self._current_session_id:
            return None
            
        ref = (f"{self._config.collection_prefix}/telemetry/{self._current_session_id}"
               f"/cars/{car_idx}/history/laps")
        return self._rtdb.child(ref).get() 

    def get_driver_stints(self, car_idx: Optional[int] = None, driver_id: Optional[str] = None) -> Dict[str, Any]:
        """Get stint information filtered by car or driver."""
        if not self._current_session_id:
            return {}
            
        stints_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/stints"
        )
        
        if car_idx is not None:
            stints_ref = stints_ref.where('car_idx', '==', car_idx)
        if driver_id is not None:
            stints_ref = stints_ref.where('driver_id', '==', driver_id)
            
        return {stint.id: stint.to_dict() for stint in stints_ref.stream()}

    def get_driver_lap_times(self, driver_id: str) -> Dict[str, Any]:
        """Get all lap times for a specific driver."""
        if not self._current_session_id:
            return {}
            
        laps_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/laps"
        ).where('driver_id', '==', driver_id)
        
        return {lap.id: lap.to_dict() for lap in laps_ref.stream()} 

    def store_collision_event(self, car_idx: int, collision_data: Dict[str, Any]):
        """Store a collision event with full details."""
        if not self._current_session_id:
            return

        # Store in Firestore for permanent record
        collision_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/collisions"
        ).document()

        collision_doc = {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'car_idx': car_idx,
            'collision_type': collision_data.get('collision_type'),
            'severity': collision_data.get('severity'),
            'incident_class': collision_data.get('incident_class'),
            'position': collision_data.get('position'),
            'impact': collision_data.get('impact'),
            'race_impact': collision_data.get('race_impact'),
            'contributing_factors': collision_data.get('contributing_factors')
        }

        self._batch.set(collision_ref, collision_doc)
        self._batch_count += 1
        if self._batch_count >= self._MAX_BATCH_SIZE:
            self.commit_batch()

        # Update session collision stats
        stats_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/collision_stats"
        self._rtdb.child(stats_ref).update({
            f"cars/{car_idx}/total_collisions": self._rtdb.child(f"{stats_ref}/cars/{car_idx}/total_collisions").get() + 1,
            f"cars/{car_idx}/last_collision": firestore.SERVER_TIMESTAMP,
            f"total_collisions": self._rtdb.child(f"{stats_ref}/total_collisions").get() + 1,
            f"collisions_by_severity/{collision_data['severity']}": 
                self._rtdb.child(f"{stats_ref}/collisions_by_severity/{collision_data['severity']}").get() + 1
        })

    def store_behavioral_analysis(self, car_idx: int, analysis_data: Dict[str, Any]):
        """Store behavioral analysis data for a car."""
        if not self._current_session_id:
            return

        behavior_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/behavior"
        ).document(f"car_{car_idx}")

        self._batch.set(behavior_ref, {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'car_idx': car_idx,
            'aggression_rating': analysis_data.get('aggression_rating'),
            'risk_taking': analysis_data.get('risk_taking'),
            'spatial_awareness': analysis_data.get('spatial_awareness'),
            'common_patterns': analysis_data.get('common_patterns')
        }, merge=True)

        self._batch_count += 1
        if self._batch_count >= self._MAX_BATCH_SIZE:
            self.commit_batch()

    def update_track_hotspots(self, hotspot_data: Dict[str, Any]):
        """Update track hotspot information."""
        if not self._current_session_id:
            return

        hotspots_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/track_analysis"
        ).document('hotspots')

        self._batch.set(hotspots_ref, {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'sectors': hotspot_data.get('sectors', {}),
            'risk_zones': hotspot_data.get('risk_zones', {}),
            'incident_clusters': hotspot_data.get('incident_clusters', [])
        }, merge=True)

        self._batch_count += 1
        if self._batch_count >= self._MAX_BATCH_SIZE:
            self.commit_batch()

    def get_car_collision_history(self, car_idx: int) -> Dict[str, Any]:
        """Get collision history for a specific car."""
        if not self._current_session_id:
            return {}

        collisions = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/collisions"
        ).where('car_idx', '==', car_idx).stream()

        return {collision.id: collision.to_dict() for collision in collisions}

    def get_session_collision_stats(self) -> Dict[str, Any]:
        """Get overall collision statistics for the session."""
        if not self._current_session_id:
            return {}

        stats_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/collision_stats"
        return self._rtdb.child(stats_ref).get() 

    def update_driver_change(self, car_idx: int, new_driver_id: str):
        """Handle a driver change event."""
        if not self._current_session_id:
            return
            
        team_id = self._car_to_team.get(car_idx)
        if not team_id:
            return
            
        old_driver_id = self._current_drivers.get(car_idx)
        if old_driver_id:
            # End the previous stint
            self._end_driver_stint(car_idx)
        
        # Start new stint
        stint_data = {
            'car_idx': car_idx,
            'team_id': team_id,
            'driver_id': new_driver_id,
            'start_time': firestore.SERVER_TIMESTAMP,
            'status': 'active',
            'laps_completed': 0,
            'best_lap': None,
            'avg_lap': None,
            'fuel_used': 0,
            'tire_set': None  # Can be updated with tire change info
        }
        
        # Update current driver tracking
        self._current_drivers[car_idx] = new_driver_id
        
        # Store stint data
        stint_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/stints"
        ).document()
        stint_ref.set(stint_data)
        
        # Update team current state
        team_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}"
        self._rtdb.child(team_ref).update({
            'current_driver': new_driver_id,
            'stint_start': firestore.SERVER_TIMESTAMP,
            'last_pit_stop': firestore.SERVER_TIMESTAMP
        })
        
        # Record driver change event
        event_ref = self._db.collection(
            f"{self._config.collection_prefix}/sessions/{self._current_session_id}/events"
        ).document()
        event_ref.set({
            'type': 'driver_change',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'team_id': team_id,
            'car_idx': car_idx,
            'old_driver': old_driver_id,
            'new_driver': new_driver_id
        })

    def _update_driver_stats(self, driver_id: str):
        """Update cumulative driver statistics."""
        if not self._current_session_id:
            return
            
        # Get all completed stints for this driver
        stints = self._db.collection_group('stints').where('driver_id', '==', driver_id).stream()
        
        total_laps = 0
        total_time = 0
        best_lap = float('inf')
        
        for stint in stints:
            stint_data = stint.to_dict()
            total_laps += stint_data.get('laps_completed', 0)
            total_time += (stint_data.get('end_time', 0) - stint_data.get('start_time', 0))
            stint_best = stint_data.get('best_lap', float('inf'))
            if stint_best < best_lap:
                best_lap = stint_best
        
        # Update driver stats
        driver_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/drivers/{driver_id}"
        self._rtdb.child(driver_ref).update({
            'total_laps': total_laps,
            'total_time': total_time,
            'best_lap': best_lap if best_lap != float('inf') else None,
            'avg_lap_time': total_time / total_laps if total_laps > 0 else None
        })

    def update_team_strategy(self, team_id: str, strategy_data: Dict[str, Any]):
        """Update team strategy information."""
        if not self._current_session_id:
            return
            
        strategy_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/strategy"
        self._rtdb.child(strategy_ref).update(strategy_data)

    def get_team_cars_status(self, team_id: str) -> Dict[str, Any]:
        """Get current status of all cars for a team."""
        if not self._current_session_id or team_id not in self._teams:
            return {}
            
        team_cars = self._teams[team_id].cars
        cars_status = {}
        
        for car_idx in team_cars:
            car_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/cars/{car_idx}/current"
            cars_status[car_idx] = self._rtdb.child(car_ref).get()
            
        return cars_status

    def get_team_driver_history(self, team_id: str) -> Dict[str, Any]:
        """Get history for all drivers in a team."""
        if not self._current_session_id or team_id not in self._teams:
            return {}
            
        team_drivers = self._teams[team_id].drivers
        driver_history = {}
        
        for driver_id in team_drivers:
            driver_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/drivers/{driver_id}"
            driver_history[driver_id] = self._rtdb.child(driver_ref).get()
            
        return driver_history 

    def update_team_status(self, car_idx: int, status_data: Dict[str, Any]):
        """Update team race status."""
        if not self._current_session_id:
            return
            
        team_id = self._car_to_team.get(car_idx)
        if not team_id:
            return
            
        team_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/race_stats"
        self._rtdb.child(team_ref).update(status_data)

    def update_strategy(self, car_idx: int, strategy_data: Dict[str, Any]):
        """Update team strategy information."""
        if not self._current_session_id:
            return
            
        team_id = self._car_to_team.get(car_idx)
        if not team_id:
            return
            
        strategy_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/teams/{team_id}/strategy"
        self._rtdb.child(strategy_ref).update(strategy_data)

    def get_team_cars_status(self, team_id: str) -> Dict[str, Any]:
        """Get current status of all cars for a team."""
        if not self._current_session_id or team_id not in self._teams:
            return {}
            
        team_cars = self._teams[team_id].cars
        cars_status = {}
        
        for car_idx in team_cars:
            car_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/cars/{car_idx}/current"
            cars_status[car_idx] = self._rtdb.child(car_ref).get()
            
        return cars_status

    def get_team_driver_history(self, team_id: str) -> Dict[str, Any]:
        """Get history for all drivers in a team."""
        if not self._current_session_id or team_id not in self._teams:
            return {}
            
        team_drivers = self._teams[team_id].drivers
        driver_history = {}
        
        for driver_id in team_drivers:
            driver_ref = f"{self._config.collection_prefix}/sessions/{self._current_session_id}/drivers/{driver_id}"
            driver_history[driver_id] = self._rtdb.child(driver_ref).get()
            
        return driver_history 