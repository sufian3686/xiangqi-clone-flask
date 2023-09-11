from flask import Blueprint

country_bp = Blueprint('country', __name__)

from social_app.country import routes
