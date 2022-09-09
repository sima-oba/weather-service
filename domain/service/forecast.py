import logging
from datetime import datetime, timedelta
from typing import List

from domain.entity import Forecast, City
from domain.repository import IForecastRepository, ICityRepository
from domain.exception import EntityNotFound


class ForecastService:
    def __init__(
        self,
        forecast_repo: IForecastRepository,
        city_repo: ICityRepository
    ):
        self._forecast_repo = forecast_repo
        self._city_repo = city_repo
        self._log = logging.getLogger(self.__class__.__name__)

    def search(
        self,
        city_id: int,
        date: datetime,
        days: int
    ) -> List[Forecast]:
        city = self._city_repo.find_by_id(city_id)

        if city is None:
            raise EntityNotFound(City, f'_id {city_id}')

        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=days)

        return self._forecast_repo.find_by_interval(city._id, start, end)

    def save(self, data: dict) -> dict:
        city_name = data.pop('city')
        state_name = data.pop('state')
        city = self._city_repo.find_by_name(city_name, state_name)

        if city is None:
            raise EntityNotFound(City, (city_name, state_name))

        forecast = Forecast.new(data)
        self._forecast_repo.remove_by_date(city._id, forecast.date_time)
        self._forecast_repo.insert(city._id, forecast)
        self._log.debug(f'Added forecast {forecast._id}')

        return forecast
