from flask import jsonify, request
from flask_restx import fields, Resource
from application.schema.observed_weather import ObservedWeatherQuerySchema
from domain.service.weather_station import WeatherStationService


def obs_weather_blueprint(api, url_prefix, service: WeatherStationService):

    ns = api.namespace(
        name='Observer weather',
        path=url_prefix,
        description='Observer weather route'
    )

    model = api.model('Observer weather', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "station_id": fields.Integer(description='Station id'),
        "measurement_date": fields.DateTime(description='Measurement date'),
        "temp": fields.Float(description='Temperature'),
        "max_temp": fields.Float(description='Max temperature'),
        "min_temp": fields.Float(description='Min temperature'),
        "avg_temp": fields.Float(description='Average temperature'),
        "insolation": fields.Integer(description='Insolation'),
        "cloudiness": fields.Integer(description='Cloudiness'),
        "humidity": fields.Float(description='Humidity'),
        "avg_humidity": fields.Float(description='Average Humidity'),
        "rain": fields.Integer(description='Rain value'),
        "wind_speed": fields.Integer(description='Wind speed'),
        "wind_direction": fields.String(description='Wind direction'),
        "gust": fields.String(description='Gust'),
        "pressure": fields.Float(description='Pressure')
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/observed_weather')
    class Observed_weather(Resource):
        @ns.doc('search_observed_data')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(model, mask='*')
        def get(self):
            obs_query_schema = ObservedWeatherQuerySchema()
            query = obs_query_schema.load(request.args.to_dict())
            stations = service.get_observed_data(**query)
            return jsonify(stations)

    @ns.route('/observed_weather/checkpoint')
    class Checkpoint(Resource):
        @ns.doc('get_checkpoint')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(model, mask='*')
        def get(self):
            checkpoint = service.get_last_update()
            return {'checkpoint': checkpoint}
