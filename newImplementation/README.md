# iRacing Team Telemetry Collector

A sophisticated telemetry collection system designed for endurance racing teams, providing real-time data collection, analysis, and team management capabilities. The system collects detailed telemetry from your team's car while maintaining basic tracking of competitors.

## System Overview

### Key Features
- Real-time telemetry collection at 60Hz
- Detailed team car monitoring
- Basic competitor tracking
- Driver stint management
- Race event tracking (collisions, penalties, etc.)
- Weather and track condition monitoring
- Historical data analysis

### Data Collection Strategy
The system employs a dual-track strategy for data collection:

1. **Team Car (Detailed Data)**:
   - Full motion telemetry (60Hz)
   - Complete car state monitoring
   - Driver inputs
   - Tire and brake temperatures
   - Fuel levels and consumption
   - Detailed lap and sector timing

2. **Other Cars (Basic Data)**:
   - Position and timing
   - Basic state information
   - Lap times
   - Gap to leader

## Firebase Data Structure

### Real-time Database (RTDB)
Used for live data and current state:

```
iracing/
└── sessions/
    └── {session_id}/
        ├── teams/
        │   └── {team_id}/
        │       ├── car_data/                # Your team's car
        │       │   ├── current/
        │       │   │   ├── basic/          # Basic telemetry
        │       │   │   │   ├── position
        │       │   │   │   ├── timing
        │       │   │   │   └── state
        │       │   │   ├── detailed/       # Detailed telemetry
        │       │   │   │   ├── motion
        │       │   │   │   ├── car_state   # Temperatures, pressures
        │       │   │   │   └── inputs      # Driver inputs
        │       │   │   └── analysis/       # Real-time analysis
        │       │   └── history/            # Recent history
        │       ├── strategy/               # Team strategy
        │       │   ├── next_driver
        │       │   ├── estimated_pit_window
        │       │   ├── fuel_remaining
        │       │   └── tire_age
        │       └── race_stats/             # Current race status
        │           ├── position
        │           ├── gap_to_leader
        │           └── last_lap
        ├── other_cars/                     # Competitor cars
        │   └── {car_idx}/
        │       ├── current/                # Basic state only
        │       │   ├── position
        │       │   ├── timing
        │       │   └── state
        │       └── laps/
        └── events/                         # Race events
            ├── driver_changes/
            ├── collisions/
            └── penalties/
```

### Firestore
Used for historical data and analysis:

```
iracing/
└── sessions/
    └── {session_id}/
        ├── teams/
        │   └── {team_id}/
        │       ├── stints/                 # Driver stint history
        │       │   └── {stint_id}/
        │       │       ├── driver_id
        │       │       ├── start_time
        │       │       ├── end_time
        │       │       └── statistics
        │       └── lap_history/            # Detailed lap data
        ├── telemetry_history/              # Historical telemetry
        └── analysis/                       # Race analysis data
```

## Setup and Configuration

### Prerequisites
- Python 3.8 or higher
- iRacing installed and running
- Firebase project with both Realtime Database and Firestore enabled
- Firebase service account credentials

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd newImplementation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Firebase:
   - Create a Firebase project
   - Enable Realtime Database and Firestore
   - Generate service account credentials
   - Copy `.env.example` to `.env` and configure:
     ```
     FIREBASE_CREDS_PATH=path/to/your/credentials.json
     FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
     ```

### Team Configuration
Configure your team in the code:
```python
team_config = TeamConfig(
    team_id="your_team_id",
    name="Your Team Name",
    car_idx=1,              # Your car's ID in the session
    drivers=["driver1", "driver2", "driver3"]  # Your driver IDs
)

firebase_config = FirebaseConfig(
    credential_path="path/to/credentials.json",
    database_url="your-firebase-url",
    teams=[team_config]
)
```

## Usage

### Starting Data Collection
```python
from src.telemetry_collector import TelemetryCollector
from src.firebase_client import FirebaseClient, FirebaseConfig

# Initialize collector
collector = TelemetryCollector(config)
collector.run()
```

### Driver Changes
When changing drivers during the race:
```python
firebase_client.update_driver_change(car_idx=1, new_driver_id="driver2")
```

### Updating Strategy
Update team strategy during the race:
```python
firebase_client.update_strategy(car_idx=1, {
    'next_driver': 'driver3',
    'estimated_pit_window': '45:00',
    'fuel_remaining': 40.5,
    'estimated_laps_remaining': 15
})
```

## Data Access Patterns

### Real-time Dashboard Data
- Team car current state: `/teams/{team_id}/car_data/current`
- Race position: `/teams/{team_id}/race_stats`
- Competitor tracking: `/other_cars/{car_idx}/current`

### Analysis Data
- Stint history: Firestore `/teams/{team_id}/stints`
- Lap history: Firestore `/teams/{team_id}/lap_history`
- Telemetry analysis: Firestore `/telemetry_history`

### Event Monitoring
- Driver changes: `/events/driver_changes`
- Incidents: `/events/collisions`
- Penalties: `/events/penalties`

## Best Practices

1. **Data Management**:
   - Use RTDB for live data
   - Use Firestore for historical data
   - Implement data cleanup for old sessions

2. **Race Strategy**:
   - Monitor fuel levels and consumption
   - Track tire wear and temperatures
   - Plan driver stints based on performance

3. **Performance Optimization**:
   - Use basic data for competitors
   - Store detailed data only for team car
   - Implement efficient querying patterns

## Contributing
[Your contribution guidelines]

## License
[Your license]

## Support
[Your support information] 