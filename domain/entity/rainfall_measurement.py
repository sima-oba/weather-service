from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from .entity import Entity


@dataclass
class AtmosphericPressure:
    at_station_level: float
    maximum: float
    minimum: float


@dataclass
class Temperature:
    dry_bulb: float
    maximum: float
    minimum: float
    dew_point: float
    dew_maximum: float
    dew_minimum: float


@dataclass
class Humidity:
    air: float
    maximum: float
    minimum: float


@dataclass
class Wind:
    clockwise_direction: float
    speed: Optional[float]
    gust_maximum: float


@dataclass
class RainfallMeasurement(Entity):
    station_id: str
    date_time: datetime
    total_rainfall: Optional[float]
    atmospheric_pressure: AtmosphericPressure
    global_radiation: Optional[float]
    temperature: Temperature
    humidity: Humidity
    wind: Wind
