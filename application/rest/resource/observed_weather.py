from flask import Blueprint, request, jsonify

from domain.service import WeatherStationService
from ...schema import ObservedWeatherQuerySchema


def get_blueprint(service: WeatherStationService) -> Blueprint:
    bp = Blueprint('Observed data', __name__, url_prefix='/observed_weather')
    obs_query_schema = ObservedWeatherQuerySchema()

    @bp.get('/')
    def search_observed_data():
        query = obs_query_schema.load(request.args.to_dict())
        stations = service.get_observed_data(**query)
        return jsonify(stations)

    @bp.get('/checkpoint')
    def get_checkpoint():
        checkpoint = service.get_last_update()
        return {'checkpoint': checkpoint}

    return bp
