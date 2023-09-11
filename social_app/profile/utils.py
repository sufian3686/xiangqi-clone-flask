import os
from flask import current_app
from werkzeug.utils import secure_filename


def get_user_friends_data(user):
    return [{
        'id': friend.id,
        'username': friend.username,
        'email': friend.email,
    } for friend in user.get_friends()]


def save_profile_picture(user, file):
    filename = get_filename_from_username(user, file)
    file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename))
    user.has_profile_picture = True


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def does_file_exist(file):
    return file and allowed_file(file.filename)


def get_filename_from_username(user, file):
    filename = f'{user.username}.{secure_filename(file.filename).rsplit(".", 1)[1].lower()}'
    return filename


def get_user_country(user):
    return {
        'name': user.country.name,
        'code': user.country.code
    }


def get_user_created_date(user):
    return user.created_on.strftime('%d %b, %Y')
