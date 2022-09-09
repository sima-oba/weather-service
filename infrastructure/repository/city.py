from pymongo.database import Database

from domain.entity.city import City, CITIES
from domain.repository import ICityRepository
from .base import BaseRepository


class CityRepository(BaseRepository[City], ICityRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(City, db["city"])

    def init_cities(self):
        for city in CITIES:
            doc = self.collection.find_one({'geoid': city['geoid']})

            if doc is None:
                doc = City.new(city).asdict()
                self.collection.insert_one(doc)

    def find_by_name(self, name: str, state: str) -> City:
        return self.find_one({"name": name, "state": state})

    def find_by_geoid(self, geoid: int) -> City:
        return self.find_one({'geoid': geoid})

    def insert(self, city: City) -> City:
        return self.add(city)
