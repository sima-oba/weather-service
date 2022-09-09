from flask import jsonify, request
from application.schema import (
    ForecastQuery,
    ObservedWeatherQuerySchema,
    RainfallQuery
)
from domain.service import (
    CityService,
    ForecastService,
    WeatherStationService,
    RainfallService
)
from application.rest.resource import utils


def configure_routes_city(app, service: CityService):

    @app.route('/cities')
    def all_cities():
        return jsonify(service.get_all())


def configure_routes_forecast(app, service: ForecastService):

    query_schema = ForecastQuery()

    @app.route('/forecast')
    def search_forecast():
        query = query_schema.load(request.args)
        forecast = service.search(**query)
        return jsonify(forecast)


def configure_routes_weather(app, service: WeatherStationService):

    @app.route('/weather_stations')
    def all_stations():
        stations = service.get_all_stations()
        return jsonify(stations)


def configure_routes_obs_weather(app, service: WeatherStationService):

    obs_query_schema = ObservedWeatherQuerySchema()

    @app.route('/observed_weather')
    def search_observed_data():
        query = obs_query_schema.load(request.args.to_dict())
        stations = service.get_observed_data(**query)
        return jsonify(stations)

    @app.route('/observed_weather/checkpoint')
    def get_checkpoint():
        checkpoint = service.get_last_update()
        return {'checkpoint': checkpoint}


def configure_routes_rainfall(app, service: RainfallService):

    query = RainfallQuery()

    @app.route('/rainfall')
    def get_stations():
        return jsonify(service.get_stations())

    @app.route('/rainfall/geojson')
    def get_stations_as_geojson():
        stations = service.get_stations()
        features = utils.export_feature_collection(stations, 'geometry')
        return jsonify(features)

    @app.route('/rainfall/<string:_id>/measurements')
    def get_station_measurements(_id: str):
        day = query.load(request.args)['day']
        return jsonify(service.get_measurements(_id, day))
