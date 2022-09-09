from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional

from domain.entity import RainfallStation, RainfallMeasurement


class IRainfallRepository(ABC):
    @abstractmethod
    def find_all_stations(self) -> List[RainfallStation]:
        pass

    @abstractmethod
    def find_station_by_code(self, code: str) -> Optional[RainfallStation]:
        pass

    @abstractmethod
    def station_exists(self, station_id: str) -> bool:
        pass

    @abstractmethod
    def add_station(self, station: RainfallStation) -> RainfallStation:
        pass

    @abstractmethod
    def update_station(self, station: RainfallStation) -> RainfallStation:
        pass

    @abstractmethod
    def find_measurements(
        self,
        station_id: str,
        day: date
    ) -> List[RainfallMeasurement]:
        pass

    @abstractmethod
    def find_measurement_by_date(
        self,
        date_time: datetime,
        station_id: str
    ) -> Optional[RainfallMeasurement]:
        pass

    @abstractmethod
    def add_measurement(
        self,
        measurement: RainfallMeasurement
    ) -> RainfallMeasurement:
        pass
