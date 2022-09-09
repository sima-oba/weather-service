from flask import Flask
from flask_restx import Api
from application.rest.resource.doc import (
    cityblueprint,
    forecastblueprint,
    weather_station_blueprint,
    obs_weather_blueprint,
    rainfall_blueprint
)


def register(app: Flask, url_prefix: str, services):
    api = Api(
        app,
        version='0.0.1',
        title='Weather Service',
        description='Weather Service rest api Documentation',
        doc=url_prefix + '/doc'
    )
    dev_prefix = '/dev' + url_prefix

    cityblueprint(api, dev_prefix, services['city'])
    forecastblueprint(api, dev_prefix, services['forecast'])
    weather_station_blueprint(api, dev_prefix, services['weather'])
    obs_weather_blueprint(api, dev_prefix, services['weather'])
    rainfall_blueprint(api, dev_prefix, services['rainfall'])
