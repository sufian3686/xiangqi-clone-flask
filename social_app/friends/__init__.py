from flask import Blueprint

friends_bp = Blueprint('friends', __name__)

from social_app.friends import routes
