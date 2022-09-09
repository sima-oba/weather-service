from flask import Blueprint, request, jsonify
from flask_cachecontrol import cache_for

from domain.service import RainfallService
from . import utils
from ...schema import RainfallQuery


def get_blueprint(service: RainfallService) -> Blueprint:
    bp = Blueprint('Rainfall', __name__, url_prefix='/rainfall')
    query = RainfallQuery()

    @bp.get('/')
    @cache_for(weeks=1)
    def get_stations():
        return jsonify(service.get_stations())

    @bp.get('/geojson')
    @cache_for(weeks=1)
    def get_stations_as_geojson():
        stations = service.get_stations()
        features = utils.export_feature_collection(stations, 'geometry')
        return jsonify(features)

    @bp.get('/<string:_id>/measurements')
    def get_station_measurements(_id: str):
        day = query.load(request.args)['day']
        return jsonify(service.get_measurements(_id, day))

    return bp
