from domain.service import ForecastService
from application.schema import ForecastSchema
from .base import BaseConsumer
from ..error import error_handler


class ForecastConsumer(BaseConsumer):
    def __init__(self, service: ForecastService):
        super().__init__()
        self._service = service
        self._schema = ForecastSchema()

    @error_handler
    def process(self, msg: any):
        data = self._schema.loads(msg.value(), many=True)

        for item in data:
            self._service.save(item)
