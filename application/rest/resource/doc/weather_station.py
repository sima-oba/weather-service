from flask import jsonify
from flask_restx import fields, Resource
from domain.service.weather_station import WeatherStationService


def weather_station_blueprint(api, url_prefix, service: WeatherStationService):

    ns = api.namespace(
        name='Stations',
        path=url_prefix,
        description='Stations route'
    )

    model = api.model('Stations', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "code": fields.Integer(description='Station code'),
        "name": fields.String(description='Name'),
        "status": fields.String(description='Status'),
        "type": fields.String(description='Type'),
        "latitude": fields.Float(description='Latitude'),
        "longitude": fields.Float(description='Longitude'),
        "altitude": fields.Float(description='Altitude'),
        "start_operation": fields.DateTime(description='Start operation'),
        "source": fields.String(description='Source'),
        "end_operation": fields.DateTime(description='End operation')
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/weather_stations')
    class Weather_station(Resource):
        @ns.doc('all_stations')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(model, mask='*')
        def get(self):
            stations = service.get_all_stations()
            return jsonify(stations)
