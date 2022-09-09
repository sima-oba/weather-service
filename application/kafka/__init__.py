from domain.service import (
    ForecastService,
    WeatherStationService,
    RainfallService
)
from infrastructure import database
from infrastructure.repository import (
    CityRepository,
    ForecastRepository,
    WeatherStationRepository,
    RainfallRepository
)
from .consumer import (
    Consumer,
    ConsumerGroup,
    ObservedWeatherConsumer
)
from ..schema import RainfallSchema, ForecastSchema


def start_consumer(config):
    db = database.get_database(config.MONGODB_SETTINGS)
    group = ConsumerGroup({
        'bootstrap.servers': config.KAFKA_SERVER,
        'group.id': 'WEATHER',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })

    rainfall_repo = RainfallRepository(db)
    rainfall_svc = RainfallService(rainfall_repo)
    rainfall_consumer = Consumer(RainfallSchema(), rainfall_svc.save)
    group.add(rainfall_consumer, 'RAINFALL')

    city_repo = CityRepository(db)
    forecast_repo = ForecastRepository(db)
    forecast_svc = ForecastService(forecast_repo, city_repo)
    forecast_consumer = Consumer(ForecastSchema(), forecast_svc.save)
    group.add(forecast_consumer, 'FORECAST')

    weather_repo = WeatherStationRepository(db)
    weather_svc = WeatherStationService(weather_repo, config.CHECKPOINT)
    observed_weather_consumer = ObservedWeatherConsumer(weather_svc)
    group.add(observed_weather_consumer, 'OBSERVED_WEATHER')

    group.wait()
