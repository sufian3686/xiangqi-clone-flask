from http import HTTPStatus
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from social_app.auth import auth_bp
from social_app.extensions import jwt
from social_app.auth.schema import RegistrationSchema, LoginSchema
from social_app.models.auth import User
from social_app.auth.utils import create_new_user, authenticate_user, get_auth_response, get_error_summary


@jwt.user_identity_loader
def user_identity_lookup(username):
    return username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@auth_bp.post('/register')
def register():
    data = request.json
    schema = RegistrationSchema()

    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        error_summary = get_error_summary(e.messages)
        return jsonify({'message': error_summary}), HTTPStatus.BAD_REQUEST

    try:
        create_new_user(**validated_data)
    except IntegrityError:
        return jsonify({'message': 'Username or Email already exists'}), HTTPStatus.CONFLICT

    return jsonify({'message': 'Account created successfully!'}), HTTPStatus.CREATED


@auth_bp.post('/login')
def login():
    data = request.json
    schema = LoginSchema()

    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        error_summary = get_error_summary(e.messages)
        return jsonify({'message': error_summary}), HTTPStatus.BAD_REQUEST

    user = authenticate_user(**validated_data)
    if not user:
        return jsonify({'message': 'Invalid username or password'}), HTTPStatus.UNAUTHORIZED

    response = get_auth_response(user)

    return jsonify(response), HTTPStatus.OK


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user,
                                           expires_delta=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES'))
    return jsonify({'access_token': new_access_token}), HTTPStatus.OK
