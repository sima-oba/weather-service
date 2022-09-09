from datetime import datetime
from flask import Flask, Blueprint
from flask_cors import CORS

from domain.service import (
    CityService,
    ForecastService,
    WeatherStationService,
    RainfallService,
)
from infrastructure import database
from infrastructure.repository import (
    CityRepository,
    ForecastRepository,
    WeatherStationRepository,
    RainfallRepository,
)
from .resource import (
    cities,
    forecast,
    observed_weather,
    rainfall,
    weather_stations,
)
from .encoder import CustomJsonEncoder
from .error import error_bp
from .resource.doc import docs
from .security import Authorization, Role


URL_PREFIX = '/api/v1/weather'


def create_server(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_SORT_KEYS'] = False
    app.url_map.strict_slashes = False
    app.json_encoder = CustomJsonEncoder
    app.register_blueprint(error_bp)

    CORS(app)
    is_auth_enabled = app.config['FLASK_ENV'] != 'development'
    auth = Authorization(config.INTROSPECTION_URI, is_auth_enabled)
    auth.grant_role_for_any_request(Role.ADMIN, Role.READ_WEATHER)
    db = database.get_database(config.MONGODB_SETTINGS)

    root_bp = Blueprint('Root', __name__, url_prefix=URL_PREFIX)

    city_repo = CityRepository(db)
    city_svc = CityService(city_repo)
    city_bp = cities.get_blueprint(city_svc)
    root_bp.register_blueprint(city_bp)

    forecast_repo = ForecastRepository(db)
    forecast_svc = ForecastService(forecast_repo, city_repo)
    forecast_bp = forecast.get_blueprint(forecast_svc)
    auth.require_authorization_for_any_request(forecast_bp)
    root_bp.register_blueprint(forecast_bp)

    checkpoint = datetime.strptime(config.CHECKPOINT, '%Y-%m-%d')
    weather_st_repo = WeatherStationRepository(db)
    weather_st_svc = WeatherStationService(weather_st_repo, checkpoint)
    weather_st_bp = weather_stations.get_blueprint(weather_st_svc)
    auth.require_authorization_for_any_request(weather_st_bp)
    root_bp.register_blueprint(weather_st_bp)

    observed_weather_bp = observed_weather.get_blueprint(weather_st_svc)
    auth.require_authorization_for_any_request(observed_weather_bp)
    root_bp.register_blueprint(observed_weather_bp)

    rainfall_repo = RainfallRepository(db)
    rainfall_svc = RainfallService(rainfall_repo)
    rainfall_bp = rainfall.get_blueprint(rainfall_svc)
    auth.require_authorization_for_any_request(rainfall_bp)
    root_bp.register_blueprint(rainfall_bp)

    docs.register(app, URL_PREFIX, {
        'city': city_svc,
        'forecast': forecast_svc,
        'weather': weather_st_svc,
        'rainfall': rainfall_svc
    })
    app.register_blueprint(root_bp)

    return app
