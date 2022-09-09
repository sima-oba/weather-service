from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

from domain.entity import Forecast


class IForecastRepository(ABC):
    @abstractmethod
    def find_by_interval(
        self, city_id: str, start_day: datetime, end_day: datetime
    ) -> List[Forecast]:
        pass

    @abstractmethod
    def insert(self, city_id: str, forecast: Forecast) -> Forecast:
        pass

    @abstractmethod
    def remove_by_date(self, city_id: str, date_time: datetime):
        pass
