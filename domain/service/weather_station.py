import logging
from typing import List
from datetime import datetime

from domain.entity import WeatherStation, ObservedWeather
from domain.repository import IWeatherStationRepository
from domain.exception import EntityNotFound


class WeatherStationService:
    def __init__(self, repo: IWeatherStationRepository, checkpoint: datetime):
        self._repo = repo
        self._initial_checkpoint = checkpoint
        self._log = logging.getLogger(self.__class__.__name__)

    def get_all_stations(self) -> List[WeatherStation]:
        return self._repo.find_all_stations()

    def get_observed_data(
        self, station_id: str, start: datetime = None, end: datetime = None
    ) -> List[ObservedWeather]:
        station = self._repo.find_station_by_id(station_id)

        if station is None:
            raise EntityNotFound('Station', station_id)

        return self._repo.find_observed_data(station._id, start, end)

    def get_last_update(self) -> datetime:
        checkpoint = self._repo.find_last_update()

        if checkpoint is None:
            return self._initial_checkpoint

        return checkpoint

    def save_observed_data(
        self,
        station_data: dict,
        obs_data: dict
    ) -> ObservedWeather:
        station = self._repo.find_station_by_code(station_data['code'])

        if station is None:
            station = WeatherStation.new(station_data)
            self._repo.insert_station(station)
            self._log.debug(f'Added weather station {station._id}')
        else:
            self._log.debug(f'Weather station {station.code} already exists')

        observed = self._repo.find_observed_data_by_datetime(
            station._id, obs_data['measurement_date']
        )

        if observed is None:
            obs_data['station_id'] = station._id
            observed = ObservedWeather.new(obs_data)
            self._repo.insert_observed_data(observed)
            self._log.debug(f'Inserted observed weather {observed._id}')
        else:
            self._log.debug(
                f'Observed weather {station._id}-{observed.measurement_date} '
                'already exists'
            )

        return observed
