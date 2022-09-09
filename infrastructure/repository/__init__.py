from pymongo.database import Database

from .forecast import ForecastRepository
from .city import CityRepository
from .weather_station import WeatherStationRepository
from .rainfall import RainfallRepository


__all__ = [
    'ForecastRepository',
    'CityRepository',
    'WeatherStationRepository',
    'RainfallRepository'
]


def init_database(db: Database):
    CityRepository(db).init_cities()
