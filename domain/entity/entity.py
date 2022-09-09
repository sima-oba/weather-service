from dataclasses import dataclass, asdict
from dacite.core import from_dict
from datetime import datetime
from uuid import uuid4


@dataclass
class Entity:
    _id: str
    created_at: datetime
    updated_at: datetime

    def asdict(self) -> dict:
        return asdict(self)

    def merge(self, data: dict):
        merged = {**self.asdict(), 'updated_at': datetime.utcnow(), **data}
        return from_dict(self.__class__, merged)

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(cls, data)

    @classmethod
    def new(cls, data: dict):
        return cls(
            _id=str(uuid4()),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **data
        )
