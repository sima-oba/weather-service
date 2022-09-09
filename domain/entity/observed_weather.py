from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .entity import Entity


@dataclass
class ObservedWeather(Entity):
    measurement_date: datetime
    temp: Optional[float]
    min_temp: Optional[float]
    max_temp: Optional[float]
    avg_temp: Optional[float]
    insolation: Optional[float]
    cloudiness: Optional[float]
    humidity: Optional[float]
    avg_humidity: Optional[float]
    rain: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    gust: Optional[float]
    pressure: Optional[float]
    station_id: str
