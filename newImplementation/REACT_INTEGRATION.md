# React.js Dashboard Integration Guide

This guide details how to integrate your React.js dashboard with the iRacing Team Telemetry Firebase structure.

## Firebase Setup

```javascript
// firebase.js
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue } from 'firebase/database';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  // Your Firebase config
};

export const app = initializeApp(firebaseConfig);
export const rtdb = getDatabase(app);
export const firestore = getFirestore(app);
```

## Data Access Patterns

### Real-time Data Hooks

```javascript
// hooks/useTeamCarData.js
import { useState, useEffect } from 'react';
import { rtdb } from '../firebase';
import { ref, onValue } from 'firebase/database';

export const useTeamCarData = (sessionId, teamId) => {
  const [carData, setCarData] = useState(null);

  useEffect(() => {
    const carRef = ref(rtdb, `iracing/sessions/${sessionId}/teams/${teamId}/car_data/current`);
    return onValue(carRef, (snapshot) => {
      setCarData(snapshot.val());
    });
  }, [sessionId, teamId]);

  return carData;
};

// hooks/useRaceStrategy.js
export const useRaceStrategy = (sessionId, teamId) => {
  const [strategy, setStrategy] = useState(null);

  useEffect(() => {
    const strategyRef = ref(rtdb, `iracing/sessions/${sessionId}/teams/${teamId}/strategy`);
    return onValue(strategyRef, (snapshot) => {
      setStrategy(snapshot.val());
    });
  }, [sessionId, teamId]);

  return strategy;
};

// hooks/useCompetitorData.js
export const useCompetitorData = (sessionId, carIdx) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const ref = ref(rtdb, `iracing/sessions/${sessionId}/other_cars/${carIdx}/current`);
    return onValue(ref, (snapshot) => {
      setData(snapshot.val());
    });
  }, [sessionId, carIdx]);

  return data;
};
```

### Historical Data Access

```javascript
// api/telemetryHistory.js
import { firestore } from '../firebase';
import { collection, query, where, getDocs } from 'firebase/firestore';

export const getLapHistory = async (sessionId, teamId, startLap, endLap) => {
  const constraints = [];
  if (startLap) constraints.push(where('lapNumber', '>=', startLap));
  if (endLap) constraints.push(where('lapNumber', '<=', endLap));

  const q = query(
    collection(firestore, `iracing/sessions/${sessionId}/teams/${teamId}/lap_history`),
    ...constraints
  );

  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => doc.data());
};

export const getDriverStints = async (sessionId, teamId) => {
  const q = query(
    collection(firestore, `iracing/sessions/${sessionId}/teams/${teamId}/stints`)
  );
  
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => doc.data());
};
```

## Example Components

### Team Car Dashboard

```javascript
// components/TeamCarDashboard.js
import React from 'react';
import { useTeamCarData, useRaceStrategy } from '../hooks';

export const TeamCarDashboard = ({ sessionId, teamId }) => {
  const carData = useTeamCarData(sessionId, teamId);
  const strategy = useRaceStrategy(sessionId, teamId);

  if (!carData) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      {/* Basic Info */}
      <div className="basic-info">
        <h2>Position: {carData.basic.position}</h2>
        <div>Last Lap: {carData.basic.timing.lastLap}</div>
        <div>Best Lap: {carData.basic.timing.bestLap}</div>
      </div>

      {/* Detailed Telemetry */}
      {carData.detailed && (
        <div className="detailed-info">
          <div>Fuel: {carData.detailed.carState.fuelLevel}L</div>
          <div>Speed: {carData.basic.state.speed}km/h</div>
          <div>RPM: {carData.basic.state.rpm}</div>
        </div>
      )}

      {/* Strategy */}
      {strategy && (
        <div className="strategy">
          <h3>Strategy</h3>
          <div>Next Driver: {strategy.nextDriver}</div>
          <div>Est. Pit Window: {strategy.estimatedPitWindow}</div>
          <div>Fuel Remaining: {strategy.fuelRemaining}L</div>
        </div>
      )}
    </div>
  );
};
```

### Competitor Tracking

```javascript
// components/CompetitorTracker.js
import React from 'react';
import { useCompetitorData } from '../hooks';

export const CompetitorTracker = ({ sessionId, competitors }) => {
  return (
    <div className="competitors">
      {competitors.map(carIdx => (
        <CompetitorCard
          key={carIdx}
          sessionId={sessionId}
          carIdx={carIdx}
        />
      ))}
    </div>
  );
};

const CompetitorCard = ({ sessionId, carIdx }) => {
  const data = useCompetitorData(sessionId, carIdx);

  if (!data) return null;

  return (
    <div className="competitor-card">
      <div>Position: {data.position}</div>
      <div>Last Lap: {data.timing.lastLap}</div>
      <div>Gap: {data.timing.gap}</div>
    </div>
  );
};
```

## Expected Data Update Frequencies

- Team Car Basic Data: ~60Hz
- Team Car Detailed Data: ~60Hz
- Competitor Data: ~10Hz
- Strategy Updates: On change
- Weather Updates: ~1Hz

## Performance Considerations

1. **Real-time Updates**:
   - Use `useCallback` for event handlers
   - Implement debouncing for high-frequency updates
   - Consider using Web Workers for heavy computations

2. **Historical Data**:
   - Implement pagination for large datasets
   - Cache frequently accessed data
   - Use query limits and filters

3. **Component Optimization**:
   - Use `React.memo()` for pure components
   - Use virtualization for long lists
   - Lazy load non-critical components

## Error Handling

```javascript
// hooks/useFirebaseError.js
export const useFirebaseError = (path) => {
  const [error, setError] = useState(null);

  useEffect(() => {
    const handleError = (error) => {
      console.error(`Firebase error at ${path}:`, error);
      setError(error);
    };

    // Implementation of error handling
    return () => {
      // Cleanup
    };
  }, [path]);

  return error;
};
```

## State Management

For complex state management, consider using Redux or Zustand to manage application state, particularly for:
- Session management
- User preferences
- Cached historical data
- UI state

## Testing

Include unit tests for your hooks and components using React Testing Library and Jest.

## Example Data Structures

Here's what to expect in the data:

```javascript
// Example team car data structure
const teamCarData = {
  basic: {
    position: 1,
    timing: {
      lastLap: 83.456,
      bestLap: 82.789,
      gap: 1.234
    },
    state: {
      gear: 4,
      speed: 210.5,
      rpm: 7800
    }
  },
  detailed: {
    motion: {
      velocity: { x: 50.1, y: 0.2, z: -0.1 },
      acceleration: { long: 1.2, lat: -0.3, vert: 0.1 }
    },
    carState: {
      fuelLevel: 45.6,
      tireTemps: [80.1, 82.3, 81.5, 79.8],
      brakeTemps: [450.2, 448.7, 445.1, 447.3]
    },
    inputs: {
      throttle: 1.0,
      brake: 0.0,
      steering: -0.2
    }
  }
};

// Example race strategy data
const strategyData = {
  nextDriver: "John Doe",
  estimatedPitWindow: "45:00",
  fuelRemaining: 40.5,
  tireAge: 12
};

// Example competitor data
const competitorData = {
  position: 2,
  timing: {
    lastLap: 83.789,
    gap: 1.234
  },
  state: {
    speed: 209.8
  }
};
```

## Real-time Updates and Event Handling

### Event Hooks

```javascript
// hooks/useRaceEvents.js
import { useState, useEffect } from 'react';
import { rtdb } from '../firebase';
import { ref, onChildAdded } from 'firebase/database';

export const useDriverChanges = (sessionId) => {
  const [changes, setChanges] = useState([]);

  useEffect(() => {
    const eventsRef = ref(rtdb, `iracing/sessions/${sessionId}/events/driver_changes`);
    return onChildAdded(eventsRef, (snapshot) => {
      const change = snapshot.val();
      setChanges(prev => [...prev, change]);
    });
  }, [sessionId]);

  return changes;
};

export const useCollisionEvents = (sessionId) => {
  const [collisions, setCollisions] = useState([]);

  useEffect(() => {
    const eventsRef = ref(rtdb, `iracing/sessions/${sessionId}/events/collisions`);
    return onChildAdded(eventsRef, (snapshot) => {
      const collision = snapshot.val();
      setCollisions(prev => [...prev, collision]);
    });
  }, [sessionId]);

  return collisions;
};

export const usePenaltyEvents = (sessionId) => {
  const [penalties, setPenalties] = useState([]);

  useEffect(() => {
    const eventsRef = ref(rtdb, `iracing/sessions/${sessionId}/events/penalties`);
    return onChildAdded(eventsRef, (snapshot) => {
      const penalty = snapshot.val();
      setPenalties(prev => [...prev, penalty]);
    });
  }, [sessionId]);

  return penalties;
};
```

### Event Components

```javascript
// components/EventFeed.js
import React from 'react';
import { useDriverChanges, useCollisionEvents, usePenaltyEvents } from '../hooks';

export const EventFeed = ({ sessionId }) => {
  const driverChanges = useDriverChanges(sessionId);
  const collisions = useCollisionEvents(sessionId);
  const penalties = usePenaltyEvents(sessionId);

  return (
    <div className="event-feed">
      <h3>Race Events</h3>
      <div className="events-list">
        {[...driverChanges, ...collisions, ...penalties]
          .sort((a, b) => b.timestamp - a.timestamp)
          .map(event => (
            <EventCard key={event.id} event={event} />
          ))}
      </div>
    </div>
  );
};

const EventCard = ({ event }) => {
  switch (event.type) {
    case 'driver_change':
      return (
        <div className="event-card driver-change">
          <div>Driver Change: {event.previousDriver} → {event.newDriver}</div>
          <div>Time: {new Date(event.timestamp).toLocaleTimeString()}</div>
        </div>
      );
    case 'collision':
      return (
        <div className="event-card collision">
          <div>Collision: Car #{event.carIdx}</div>
          <div>Severity: {event.severity}</div>
          <div>Time: {new Date(event.timestamp).toLocaleTimeString()}</div>
        </div>
      );
    case 'penalty':
      return (
        <div className="event-card penalty">
          <div>Penalty: Car #{event.carIdx}</div>
          <div>Type: {event.penaltyType}</div>
          <div>Time: {new Date(event.timestamp).toLocaleTimeString()}</div>
        </div>
      );
    default:
      return null;
  }
};

### High-Frequency Updates

For handling high-frequency telemetry updates (60Hz), consider these optimization techniques:

```javascript
// hooks/useThrottledCarData.js
import { useState, useEffect, useCallback } from 'react';
import { rtdb } from '../firebase';
import { ref, onValue } from 'firebase/database';
import { throttle } from 'lodash';

export const useThrottledCarData = (sessionId, teamId, fps = 10) => {
  const [carData, setCarData] = useState(null);

  // Throttle updates to specified FPS
  const throttledUpdate = useCallback(
    throttle((newData) => {
      setCarData(newData);
    }, 1000 / fps),
    []
  );

  useEffect(() => {
    const carRef = ref(rtdb, `iracing/sessions/${sessionId}/teams/${teamId}/car_data/current`);
    return onValue(carRef, (snapshot) => {
      throttledUpdate(snapshot.val());
    });
  }, [sessionId, teamId, throttledUpdate]);

  return carData;
};
```

### WebWorker for Heavy Computations

```javascript
// workers/telemetryWorker.js
self.onmessage = (e) => {
  const { telemetryData } = e.data;
  
  // Perform heavy computations
  const processed = processTelemetryData(telemetryData);
  
  self.postMessage(processed);
};

function processTelemetryData(data) {
  // Example processing
  return {
    avgSpeed: calculateMovingAverage(data.speeds, 10),
    fuelTrend: calculateFuelConsumptionTrend(data.fuelLevels),
    // ... other computations
  };
}

// hooks/useProcessedTelemetry.js
export const useProcessedTelemetry = (telemetryData) => {
  const [processed, setProcessed] = useState(null);
  const workerRef = useRef();

  useEffect(() => {
    workerRef.current = new Worker('telemetryWorker.js');
    workerRef.current.onmessage = (e) => {
      setProcessed(e.data);
    };

    return () => workerRef.current.terminate();
  }, []);

  useEffect(() => {
    if (telemetryData) {
      workerRef.current.postMessage({ telemetryData });
    }
  }, [telemetryData]);

  return processed;
};
``` 