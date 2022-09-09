from typing import List, Optional
from abc import ABC, abstractmethod
from datetime import datetime

from domain.entity import WeatherStation, ObservedWeather


class IWeatherStationRepository(ABC):
    @abstractmethod
    def find_all_stations(self) -> List[WeatherStation]:
        pass

    def find_station_by_id(self, id: str) -> WeatherStation:
        pass

    @abstractmethod
    def find_station_by_code(self, code: str) -> WeatherStation:
        pass

    @abstractmethod
    def insert_station(self, station: WeatherStation) -> WeatherStation:
        pass

    @abstractmethod
    def find_observed_data(
        self,
        station_id: str,
        start: datetime = None,
        end: datetime = None
    ) -> List[ObservedWeather]:
        pass

    @abstractmethod
    def find_observed_data_by_datetime(
        self,
        station_id: str,
        date_time: datetime
    ) -> Optional[ObservedWeather]:
        pass

    @abstractmethod
    def insert_observed_data(self, data: ObservedWeather) -> ObservedWeather:
        pass

    @abstractmethod
    def find_last_update(self) -> datetime:
        pass
