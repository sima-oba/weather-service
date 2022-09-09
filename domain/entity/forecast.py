from dataclasses import dataclass
from datetime import datetime

from .entity import Entity


@dataclass
class Forecast(Entity):
    date_time: datetime
    weather: str
    summary: str
    max_temp: int
    max_temp_trend: str
    min_temp: int
    min_temp_trend: str
    max_humidity: int
    min_humidity: int
    wind_direction: str
    wind_speed: str
    season: str
    sunrise: datetime
    sunset: datetime
    source: str
