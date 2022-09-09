from http import HTTPStatus
from flask import Blueprint, jsonify
from marshmallow import ValidationError

from domain.exception import EntityNotFound


error_bp = Blueprint('Error handling', __name__)


@error_bp.app_errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify(error.messages), HTTPStatus.BAD_REQUEST


@error_bp.app_errorhandler(EntityNotFound)
def handle_entity_not_found(error: EntityNotFound):
    return jsonify({'error': str(error)}), HTTPStatus.NOT_FOUND
