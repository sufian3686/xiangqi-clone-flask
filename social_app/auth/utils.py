from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token

from social_app.extensions import db, bcrypt
from social_app.models.auth import User


def create_new_user(username, email, password, country_code):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, country_code=country_code)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError("Username or Email already exists", params={}, orig=e)


def authenticate_user(username, password):
    user = User.query.filter_by(username=username.lower()).first()
    if not user or not user.is_valid_user(password):
        return None

    return user


def get_error_summary(error_messages):
    error_summary = ", ".join([f"{field}: {', '.join(errors)}" for field, errors in error_messages.items()])
    return error_summary


def get_auth_response(user):
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    user_data = {
        "username": user.username,
        "email": user.email,
    }

    return {'user': user_data, 'access_token': access_token, 'refresh_token': refresh_token}
