from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from social_app.auth import routes
