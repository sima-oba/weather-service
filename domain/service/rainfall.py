import logging
from datetime import date
from typing import List, Tuple

from ..entity import RainfallStation, RainfallMeasurement
from ..exception import EntityNotFound
from ..repository import IRainfallRepository


class RainfallService:
    def __init__(self, repo: IRainfallRepository):
        self._repo = repo
        self._log = logging.getLogger(self.__class__.__name__)

    def get_stations(self) -> List[RainfallStation]:
        return self._repo.find_all_stations()

    def get_measurements(
        self,
        station_id: str,
        from_day: date
    ) -> List[RainfallMeasurement]:
        if not self._repo.station_exists(station_id):
            raise EntityNotFound(RainfallStation, station_id)

        return self._repo.find_measurements(station_id, from_day)

    def save(self, data: dict) -> Tuple[RainfallStation, RainfallMeasurement]:
        station_data = data['station']
        msr_data = data['measurement']

        station = self.save_station(station_data)
        measurement = self.save_measurement(msr_data, station._id)

        return station, measurement

    def save_station(self, data) -> RainfallStation:
        station = self._repo.find_station_by_code(data['code'])

        if station is None:
            station = RainfallStation.new(data)
            self._repo.add_station(station)
            self._log.debug(f'Added rainfall station {station._id}')
        else:
            station = station.merge(data)
            self._repo.update_station(station)
            self._log.debug(f'Updated rainfall station {station._id}')

        return station

    def save_measurement(self, data, station_id) -> RainfallMeasurement:
        msr_datetime = data['date_time']
        msr = self._repo.find_measurement_by_date(msr_datetime, station_id)

        if msr is None:
            data['station_id'] = station_id
            msr = RainfallMeasurement.new(data)
            self._repo.add_measurement(msr)
            self._log.debug(f'Added rainfall measurement {msr._id}')
        else:
            self._log.debug(
                'Rainfall measurement already exists. '
                f'Station: {station_id}. Datetime: {msr_datetime}'
            )

        return msr
