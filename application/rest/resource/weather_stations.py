from flask import Blueprint, jsonify
from flask_cachecontrol import cache_for

from domain.service import WeatherStationService


def get_blueprint(service: WeatherStationService) -> Blueprint:
    bp = Blueprint('Stations', __name__, url_prefix='/weather_stations')

    @bp.get('/')
    @cache_for(weeks=1)
    def all_stations():
        stations = service.get_all_stations()
        return jsonify(stations)

    return bp
