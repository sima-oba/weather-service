from typing import List
from datetime import datetime
from pymongo.database import Database

from domain.entity import Forecast
from domain.repository import IForecastRepository
from .base import BaseRepository


class ForecastRepository(BaseRepository[Forecast], IForecastRepository):
    def __init__(self, db: Database):
        super().__init__(Forecast, db["forecast"])

    def find_by_interval(
        self, city_id: str, start_day: datetime, end_day: datetime
    ) -> List[Forecast]:
        return self.find_all(
            {
                "city_id": city_id,
                "date_time": {"$gte": start_day, "$lte": end_day},
            }
        )

    def insert(self, city_id: str, forecast: Forecast) -> Forecast:
        return self.add(forecast, city_id=city_id)

    def remove_by_date(self, city_id: str, date_time: datetime):
        start = date_time.replace(minute=0, second=0)
        end = date_time.replace(minute=59, second=59)
        self.remove_all(
            {'city_id': city_id, 'date_time': {'$gte': start, '$lte': end}}
        )
