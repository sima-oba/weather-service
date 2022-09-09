import logging
from typing import List

from domain.entity import City
from domain.repository import ICityRepository


class CityService:
    def __init__(self, repo: ICityRepository):
        self._repo = repo
        self._log = logging.getLogger(self.__class__.__name__)

    def get_all(self) -> List[City]:
        return self._repo.find_all()

    def save(self, data: dict) -> City:
        city = self._repo.find_by_geoid(data['geoid'])

        if city is None:
            city = self._repo.insert(City.new(data))
            self._log.debug(f'Added City {city.name} with ID {city._id}')
            return city

        self._log.debug(f'City {city.name} already exists. Skipping...')
        return city
