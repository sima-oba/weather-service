from dataclasses import dataclass
from datetime import datetime

from .entity import Entity


@dataclass
class WeatherStation(Entity):
    code: str
    name: str
    status: str
    type: str
    latitude: float
    longitude: float
    altitude: float
    start_operation: datetime
    end_operation: datetime
    source: str
