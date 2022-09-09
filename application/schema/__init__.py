from .forecast import ForecastSchema, ForecastQuery
from .observed_weather import ObservedWeatherSchema, ObservedWeatherQuerySchema
from .rainfall import RainfallSchema, RainfallQuery

__all__ = [
    'ForecastSchema',
    'ObservedWeatherSchema',
    'ObservedWeatherQuerySchema',
    'ForecastQuery',
    'RainfallSchema',
    'RainfallQuery'
]
