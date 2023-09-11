import os
from datetime import timedelta
from http import HTTPStatus

from dotenv import load_dotenv

from flask import Flask, jsonify

from social_app.exceptions import FriendOperationException, NotAllowedException
from social_app.profile import profile_bp
from social_app.friends import friends_bp
from social_app.country import country_bp
from social_app.sockets import socket_bp
from social_app.auth import auth_bp
from social_app.extensions import db, jwt, migrate, socketio, cors

load_dotenv()


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_prefixed_env()
    app.config['WTF_CSRF_ENABLED'] = False

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
        minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_MINUTES')))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(
        days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS')))

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(friends_bp)
    app.register_blueprint(socket_bp)
    app.register_blueprint(country_bp)

    with app.app_context():
        db.create_all()

    @app.errorhandler(FriendOperationException)
    def handle_friend_operation_exception(error):
        response = jsonify({'message': str(error)})
        response.status_code = HTTPStatus.BAD_REQUEST
        return response

    @app.errorhandler(NotAllowedException)
    def handle_authorization_exception(error):
        response = jsonify({'message': str(error)})
        response.status_code = HTTPStatus.FORBIDDEN
        return response

    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0")
