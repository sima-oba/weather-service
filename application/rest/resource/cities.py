from flask import Blueprint, jsonify
from flask_cachecontrol import cache_for

from domain.service import CityService


def get_blueprint(service: CityService) -> Blueprint:
    bp = Blueprint('Cities', __name__, url_prefix='/cities')

    @bp.get('/')
    @cache_for(weeks=1)
    def all_cities():
        return jsonify(service.get_all())

    return bp
