from flask import jsonify, request
from flask_restx import fields, Resource
from application.rest.resource import utils
from application.schema.rainfall import RainfallQuery
from domain.service.rainfall import RainfallService


def rainfall_blueprint(api, url_prefix, service: RainfallService):

    ns = api.namespace(
        name='Rainfall',
        path=url_prefix,
        description='Rainfall route'
    )

    geometry = api.model(
        'Geometry', {
            'type': fields.String,
            'coordinates': fields.List(fields.Integer)
        }
    )

    rainfall_station_model = api.model('RainfallStation', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "code": fields.String(description='Code'),
        "city": fields.String(description='City'),
        "state": fields.String(description='State'),
        "altitude": fields.Float(description='Altitude'),
        "geometry": fields.Nested(geometry)
    })

    rainfall_measurement_model = api.model('RainfallMeasurement', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "station_id": fields.String(description='Station id'),
        "date_time": fields.DateTime(description='Date time'),
        "total_rainfall": fields.Float(description='Total rainfall'),
        "global_radiation": fields.Float(description='Global radiation'),
        "atmospheric_pressure": fields.Nested(
            api.model('Atmospheric_Pressure', {
                "at_station_level": fields.Float(),
                "maximum": fields.Float(),
                "minimum": fields.Float()
            })
        ),
        "temperature": fields.Nested(
            api.model('temperature', {
                "dry_bulb": fields.Float(),
                "maximum": fields.Float(),
                "minimum": fields.Float(),
                "dew_point": fields.Float(),
                "dew_maximum": fields.Float(),
                "dew_minimum": fields.Float()
            })
        ),
        "humidity": fields.Nested(
            api.model('humidity', {
                "air": fields.Float(),
                "maximum": fields.Float(),
                "minimum": fields.Float()
            })
        ),
        "wind": fields.Nested(
            api.model('wind', {
                "clockwise_direction": fields.Float(),
                "speed": fields.Float(),
                "gust_maximum": fields.Float()
            })
        )
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/rainfall')
    class Rainfall(Resource):
        @ns.doc('get_stations')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(rainfall_station_model, mask='*')
        def get(self):
            return jsonify(service.get_stations())

    @ns.route('/rainfall/geojson')
    class Geojson(Resource):
        @ns.doc('get_stations_as_geojson')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(rainfall_station_model, mask='*')
        def get(self):
            stations = service.get_stations()
            features = utils.export_feature_collection(stations, 'geometry')
            return jsonify(features)

    @ns.route('rainfall/<string:_id>/measurements')
    class Measurements(Resource):
        @ns.doc('get_station_measurements', params={'_id': 'Id'})
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(rainfall_measurement_model, mask='*')
        def get(self, _id: str):
            query = RainfallQuery()
            day = query.load(request.args)['day']
            return jsonify(service.get_measurements(_id, day))
