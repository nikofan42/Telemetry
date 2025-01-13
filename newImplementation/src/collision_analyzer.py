from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import math
import time
from .firebase_client import FirebaseClient

@dataclass
class CollisionConfig:
    """Configuration for collision detection and analysis."""
    acceleration_threshold: Dict[str, float]
    proximity_check: Dict[str, Any]
    orientation_check: Dict[str, Any]
    cooldown: Dict[str, float]
    classification: Dict[str, Any]
    track_analysis: Dict[str, Any]

class CollisionAnalyzer:
    """Analyzes and records collision events in iRacing."""
    
    def __init__(self, config: CollisionConfig, firebase_client: FirebaseClient):
        self._config = config
        self._fb_client = firebase_client
        self._last_collision_time = {}  # By car_idx
        self._car_states = {}  # Track car states for analysis
        self._track_hotspots = {}  # Track incident locations
        
    def update_car_state(self, car_idx: int, telemetry_data: Dict[str, Any]):
        """Update stored car state with new telemetry data."""
        if car_idx not in self._car_states:
            self._car_states[car_idx] = {}
            
        self._car_states[car_idx].update(telemetry_data)
        self._check_for_collision(car_idx)
        
    def _check_for_collision(self, car_idx: int):
        """Check if current car state indicates a collision."""
        if not self._can_trigger_collision(car_idx):
            return
            
        car_data = self._car_states[car_idx]
        
        # Check acceleration thresholds
        if self._exceeds_acceleration_threshold(car_data):
            nearby_cars = self._find_nearby_cars(car_idx, car_data)
            
            if nearby_cars:
                collision_data = self._analyze_collision(car_idx, car_data, nearby_cars)
                self._fb_client.store_collision_event(car_idx, collision_data)
                self._update_track_hotspots(collision_data)
                self._last_collision_time[car_idx] = time.time()
                
    def _can_trigger_collision(self, car_idx: int) -> bool:
        """Check if enough time has passed since last collision."""
        current_time = time.time()
        last_time = self._last_collision_time.get(car_idx, 0)
        return (current_time - last_time) > self._config.cooldown['same_car']
        
    def _exceeds_acceleration_threshold(self, car_data: Dict[str, Any]) -> bool:
        """Check if acceleration exceeds collision thresholds."""
        accel = car_data.get('motion', {}).get('acceleration', {})
        thresholds = self._config.acceleration_threshold
        
        return (
            abs(accel.get('long', 0)) > thresholds['longitudinal'] or
            abs(accel.get('lat', 0)) > thresholds['lateral'] or
            abs(accel.get('vert', 0)) > thresholds['vertical']
        )
        
    def _find_nearby_cars(self, car_idx: int, car_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find cars in close proximity that might be involved in collision."""
        nearby_cars = []
        car_pos = car_data.get('position', {})
        
        for other_idx, other_data in self._car_states.items():
            if other_idx == car_idx:
                continue
                
            other_pos = other_data.get('position', {})
            distance = self._calculate_distance(car_pos, other_pos)
            
            if distance < self._config.proximity_check['warning_zones']['critical']:
                nearby_cars.append({
                    'car_idx': other_idx,
                    'data': other_data,
                    'distance': distance
                })
                
        return nearby_cars
        
    def _analyze_collision(self, car_idx: int, car_data: Dict[str, Any], 
                         nearby_cars: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze collision details and classify the incident."""
        # Find the closest car as the likely collision partner
        collision_partner = min(nearby_cars, key=lambda x: x['distance'])
        
        # Calculate impact details
        impact = self._calculate_impact(car_data, collision_partner['data'])
        
        # Classify the incident
        incident_class = self._classify_incident(car_data, collision_partner['data'])
        
        # Analyze contributing factors
        factors = self._analyze_contributing_factors(car_data, collision_partner['data'])
        
        return {
            'collision_type': self._determine_collision_type(impact),
            'severity': self._calculate_severity(impact),
            'incident_class': incident_class,
            'position': car_data.get('position', {}),
            'impact': impact,
            'race_impact': self._assess_race_impact(car_data),
            'contributing_factors': factors,
            'other_car_idx': collision_partner['car_idx']
        }
        
    def _calculate_impact(self, car_data: Dict[str, Any], 
                         other_car_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate impact forces and changes in car state."""
        return {
            'velocity_delta': self._calculate_velocity_delta(
                car_data.get('motion', {}).get('velocity', {}),
                other_car_data.get('motion', {}).get('velocity', {})
            ),
            'peak_acceleration': car_data.get('motion', {}).get('acceleration', {}),
            'orientation_change': self._calculate_orientation_change(car_data)
        }
        
    def _calculate_severity(self, impact: Dict[str, Any]) -> str:
        """Determine collision severity based on impact data."""
        accel_magnitude = math.sqrt(
            impact['peak_acceleration'].get('long', 0)**2 +
            impact['peak_acceleration'].get('lat', 0)**2 +
            impact['peak_acceleration'].get('vert', 0)**2
        )
        
        thresholds = self._config.classification['impact_categories']
        
        if accel_magnitude >= thresholds['heavy']:
            return 'heavy'
        elif accel_magnitude >= thresholds['medium']:
            return 'medium'
        else:
            return 'light'
            
    def _update_track_hotspots(self, collision_data: Dict[str, Any]):
        """Update track hotspot analysis with new collision data."""
        position = collision_data.get('position', {})
        track_pct = position.get('track_pct', 0)
        sector = int(track_pct / self._config.track_analysis['sector_size'])
        
        if sector not in self._track_hotspots:
            self._track_hotspots[sector] = {
                'collisions': 0,
                'severity_sum': 0,
                'common_types': [],
                'risk_factor': 1.0
            }
            
        hotspot = self._track_hotspots[sector]
        hotspot['collisions'] += 1
        hotspot['severity_sum'] += (
            2 if collision_data['severity'] == 'heavy'
            else 1 if collision_data['severity'] == 'medium'
            else 0.5
        )
        hotspot['common_types'].append(collision_data['collision_type'])
        
        # Update Firebase with new hotspot data
        self._fb_client.update_track_hotspots({
            'sectors': self._track_hotspots,
            'risk_zones': self._calculate_risk_zones()
        })
        
    def _calculate_risk_zones(self) -> Dict[str, Any]:
        """Calculate high-risk zones based on collision history."""
        risk_zones = {}
        for sector, data in self._track_hotspots.items():
            risk_factor = (data['collisions'] * data['severity_sum'] * 
                         self._config.track_analysis['risk_zones'].get(
                             self._get_sector_type(sector), 1.0
                         ))
            risk_zones[str(sector)] = risk_factor
        return risk_zones
        
    @staticmethod
    def _calculate_distance(pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
        """Calculate distance between two positions."""
        return math.sqrt(
            (pos1.get('x', 0) - pos2.get('x', 0))**2 +
            (pos1.get('y', 0) - pos2.get('y', 0))**2 +
            (pos1.get('z', 0) - pos2.get('z', 0))**2
        )
        
    @staticmethod
    def _calculate_velocity_delta(vel1: Dict[str, float], 
                                vel2: Dict[str, float]) -> Dict[str, float]:
        """Calculate relative velocity between two cars."""
        return {
            'x': vel1.get('x', 0) - vel2.get('x', 0),
            'y': vel1.get('y', 0) - vel2.get('y', 0),
            'z': vel1.get('z', 0) - vel2.get('z', 0)
        } 