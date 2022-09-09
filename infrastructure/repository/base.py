from dataclasses import fields
from pymongo.database import Collection
from typing import Generic, TypeVar, Union, Type, List

from domain.entity.entity import Entity


T = TypeVar('T', bound=Entity)


class BaseRepository(Generic[T]):
    def __init__(self, cls: Type[T], collection: Collection):
        self._cls = cls
        self._cls_fields = fields(cls)
        self.collection = collection

    def _as_entity(self, doc: dict) -> T:
        doc = {f.name: doc.get(f.name) for f in self._cls_fields}
        return self._cls(**doc)

    def _as_list(self, cursor: any) -> List[T]:
        return [self._as_entity(it) for it in cursor]

    def aggregate(self, pipeline: List[dict]) -> List[T]:
        docs = self.collection.aggregate(pipeline)
        return self._as_list(docs)

    def find_all(self, filter: dict = None) -> List[T]:
        docs = self.collection.find(filter)
        return self._as_list(docs)

    def find_one(self, filter: dict) -> Union[T, None]:
        doc = self.collection.find_one(filter)
        return self._as_entity(doc) if doc else None

    def find_by_id(self, id: str) -> Union[T, None]:
        return self.find_one({'_id': id})

    def add(self, entity: T, **kwargs) -> T:
        result = self.collection.insert_one({**entity.asdict(), **kwargs})
        entity._id = result.inserted_id
        return entity

    def remove_all(self, filter: dict) -> bool:
        result = self.collection.delete_many(filter)
        return result.deleted_count > 0
