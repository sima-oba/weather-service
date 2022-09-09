from dataclasses import dataclass

from .entity import Entity
from .geometry import Geometry


@dataclass
class RainfallStation(Entity):
    code: str
    city: str
    state: str
    altitude: float
    geometry: Geometry
