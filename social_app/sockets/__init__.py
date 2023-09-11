from flask import Blueprint

socket_bp = Blueprint('sockets', __name__)

from social_app.sockets import sockets
