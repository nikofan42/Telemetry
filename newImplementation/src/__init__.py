"""
iRacing Telemetry Collector package.

This package provides tools for collecting and storing iRacing telemetry data
in Firebase, supporting both real-time updates and historical data storage.
"""

from .iracing_client import IRacingClient
from .firebase_client import FirebaseClient, FirebaseConfig
from .telemetry_collector import TelemetryCollector, CollectorConfig

__version__ = '0.1.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

__all__ = [
    'IRacingClient',
    'FirebaseClient',
    'FirebaseConfig',
    'TelemetryCollector',
    'CollectorConfig'
] 