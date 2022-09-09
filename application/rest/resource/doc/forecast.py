from flask import jsonify, request
from flask_restx import fields, Resource
from application.schema.forecast import ForecastQuery
from domain.service.forecast import ForecastService


def forecastblueprint(api, url_prefix, service: ForecastService):

    ns = api.namespace(
        name='Forecast',
        path=url_prefix,
        description='Forecast route'
    )

    model = api.model('Forecast', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "date_time": fields.DateTime(description='Time that occurred'),
        "max_humidity": fields.Integer(description='Maximum humidity value'),
        "max_temp": fields.Integer(description='Maximum temperature'),
        "max_temp_trend": fields.Integer(
            description='Maximum temperature trending'),
        "min_humidity": fields.Integer(description='Minimum humidity value'),
        "min_temp": fields.Integer(description='Minimum temperature'),
        "min_temp_trend": fields.Integer(
            description='Minimum temperature trending'),
        "season": fields.String(description='Season'),
        "source": fields.String(description='Source'),
        "summary": fields.String(description='Summary'),
        "sunrise": fields.DateTime(description='Sunrise'),
        "sunset": fields.DateTime(description='Sunset'),
        "weather": fields.String(description='Weather'),
        "wind_direction": fields.String(description='Wind direction'),
        "wind_speed": fields.String(description='Wind speed'),
        "city_id": fields.String(description='The city id')
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/forecast')
    class Forecast(Resource):
        @ns.doc('search_forecast')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(model, mask='*')
        def get(self):
            query_schema = ForecastQuery()
            query = query_schema.load(request.args)
            forecast = service.search(**query)
            return jsonify(forecast)
