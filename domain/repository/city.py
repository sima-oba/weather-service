from typing import List
from abc import ABC, abstractmethod

from domain.entity import City


class ICityRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[City]:
        pass

    @abstractmethod
    def find_by_id(self, city_id: str) -> City:
        pass

    @abstractmethod
    def find_by_geoid(self, geoid: int) -> City:
        pass

    @abstractmethod
    def find_by_name(self, name: str, state: str) -> City:
        pass

    @abstractmethod
    def insert(self, city: City) -> City:
        pass
