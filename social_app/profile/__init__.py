from flask import Blueprint

profile_bp = Blueprint('profile', __name__)

from social_app.profile import routes
