from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user

from social_app.extensions import db
from social_app.models.auth import User
from social_app.profile.schema import UserSchema
from social_app.profile.utils import does_file_exist, save_profile_picture
from social_app.profile import profile_bp


@profile_bp.get('/@<username>')
@jwt_required()
def user_profile(username=None):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), HTTPStatus.NOT_FOUND

    schema = UserSchema()
    user_data = schema.dump(user)
    return jsonify(user_data), HTTPStatus.OK


@profile_bp.put('/profile')
@jwt_required()
def update_user_profile():
    data = request.form.to_dict()
    file = request.files.get('profile_picture')

    if does_file_exist(file):
        save_profile_picture(current_user, file)

    current_user.bio = data.get('bio', current_user.bio)

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), HTTPStatus.OK
