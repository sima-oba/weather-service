from typing import List, Optional
from datetime import datetime
from pymongo.database import Database

from domain.entity import WeatherStation, ObservedWeather
from domain.repository import IWeatherStationRepository


class WeatherStationRepository(IWeatherStationRepository):
    def __init__(self, db: Database):
        self._stations = db['station']
        self._data = db['observed_data']

    def find_all_stations(self) -> List[WeatherStation]:
        docs = self._stations.find()
        return [WeatherStation(**item) for item in docs]

    def find_station_by_id(self, id: str) -> WeatherStation:
        doc = self._stations.find_one({'_id': id})
        return WeatherStation(**doc) if doc else None

    def find_station_by_code(self, code: str) -> WeatherStation:
        doc = self._stations.find_one({'code': code})
        return WeatherStation(**doc) if doc else None

    def insert_station(self, station: WeatherStation) -> WeatherStation:
        result = self._stations.insert_one(station.asdict())
        station._id = result.inserted_id

        return station

    def find_observed_data(
        self,
        station_id: str,
        start: datetime = None,
        end: datetime = None
    ) -> List[ObservedWeather]:
        query = {'station_id': station_id}
        measurement_date = {}

        # Consider improve filtering logic
        if start:
            measurement_date['$gte'] = start
        if end:
            measurement_date['$lte'] = end
        if measurement_date:
            query['measurement_date'] = measurement_date

        docs = self._data.find(query)
        return [ObservedWeather.from_dict(doc) for doc in docs]

    def find_observed_data_by_datetime(
        self,
        station_id: str,
        date_time: datetime
    ) -> Optional[ObservedWeather]:
        doc = self._data.find_one({
            'station_id': station_id,
            'measurement_date': date_time
        })

        return ObservedWeather.from_dict(doc) if doc else None

    def find_last_update(self) -> datetime:
        results = self._data.aggregate([
            {'$sort': {'measurement_date': -1}},
            {'$limit': 1}
        ])

        if not results._has_next():
            return None

        doc = results.next()
        return doc['measurement_date']

    def insert_observed_data(self, data: ObservedWeather) -> ObservedWeather:
        result = self._data.insert_one(data.asdict())
        data._id = result.inserted_id
        return data
