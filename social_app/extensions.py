from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()
