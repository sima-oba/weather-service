from domain.service import WeatherStationService
from application.schema import ObservedWeatherSchema
from .base import BaseConsumer
from ..error import error_handler


class ObservedWeatherConsumer(BaseConsumer):
    def __init__(self, service: WeatherStationService):
        super().__init__()
        self._service = service
        self._schema = ObservedWeatherSchema()

    @error_handler
    def process(self, msg: any):
        station, obs_data = self._schema.loads(msg.value())
        obs_data = self._service.save_observed_data(station, obs_data)
