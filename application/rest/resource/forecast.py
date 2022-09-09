from flask import Blueprint, request, jsonify

from application.schema.forecast import ForecastQuery
from domain.service import ForecastService


def get_blueprint(service: ForecastService) -> Blueprint:
    bp = Blueprint('Forecast', __name__, url_prefix='/forecast')
    query_schema = ForecastQuery()

    @bp.get('/')
    def search_forecast():
        query = query_schema.load(request.args)
        forecast = service.search(**query)
        return jsonify(forecast)

    return bp
