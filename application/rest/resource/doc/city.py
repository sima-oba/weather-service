from flask import jsonify
from flask_restx import fields, Resource
from domain.service.city import CityService


def cityblueprint(api, url_prefix, service: CityService):

    ns = api.namespace(
        name='City',
        path=url_prefix,
        description='Cities route'
    )

    citymodel = api.model('City', {
        "_id": fields.String(description='ID'),
        "created_at": fields.DateTime(description='The creation date'),
        "updated_at": fields.DateTime(description='The update date'),
        "geoid": fields.Integer(description='Geographical id'),
        "name": fields.String(description='City name'),
        "state": fields.String(description='City state')
    })

    autherrormodel = api.model(
        'Error Unauthorized',
        {"message": fields.String()}
    )

    @ns.route('/cities')
    class Cities(Resource):
        @ns.doc('all_cities')
        @ns.response(401, 'Unauthorized', model=autherrormodel)
        @ns.marshal_with(citymodel, mask='*')
        def get(self):
            return jsonify(service.get_all())
