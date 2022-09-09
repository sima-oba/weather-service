from datetime import datetime, date
from pymongo.database import Database
from typing import List, Optional

from domain.entity import RainfallStation, RainfallMeasurement
from domain.repository import IRainfallRepository


class RainfallRepository(IRainfallRepository):
    def __init__(self, database: Database):
        self._stations = database['rainfall_stations']
        self._measurements = database['rainfall_measurements']

    def station_exists(self, station_id: str) -> bool:
        doc = self._stations.find_one({'_id': station_id})
        return doc is not None

    def find_all_stations(self) -> List[RainfallStation]:
        return [
            RainfallStation.from_dict(doc)
            for doc in self._stations.find()
        ]

    def find_station_by_code(self, code: str) -> Optional[RainfallStation]:
        doc = self._stations.find_one({'code': code})
        return RainfallStation.from_dict(doc) if doc else None

    def add_station(self, station: RainfallStation) -> RainfallStation:
        self._stations.insert_one(station.asdict())
        return station

    def update_station(self, station: RainfallStation) -> RainfallStation:
        self._stations.replace_one({'_id': station._id}, station.asdict())
        return station

    def measurement_exists(self, station_id: str, date_time: datetime) -> bool:
        doc = self._measurements.find_one({
            'station_id': station_id,
            'date_time': date_time
        })
        return doc is not None

    def find_measurements(
        self,
        station_id: str,
        day: date
    ) -> List[RainfallMeasurement]:
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())

        docs = self._measurements.find({
            'station_id': station_id,
            'date_time': {'$gte': start, '$lte': end}
        })

        return [RainfallMeasurement.from_dict(doc) for doc in docs]

    def find_measurement_by_date(
        self,
        date_time: datetime,
        station_id: str
    ) -> Optional[RainfallMeasurement]:
        doc = self._measurements.find_one({
            'station_id': station_id,
            'date_time': date_time
        })

        return RainfallMeasurement.from_dict(doc) if doc else None

    def add_measurement(
        self,
        measurement: RainfallMeasurement
    ) -> RainfallMeasurement:
        self._measurements.insert_one(measurement.asdict())
        return measurement
