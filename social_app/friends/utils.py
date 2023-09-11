from flask_jwt_extended import current_user

from social_app.models.auth import User
from social_app.profile.utils import get_user_country


def get_friends_data():
    friends = current_user.get_friends()
    return [{'id': friend.id,
             'username': friend.username,
             'email': friend.email,
             'country': get_user_country(friend),
             'profile_picture': friend.get_profile_picture_url()
             } for friend in friends]


def get_non_friends_data():
    non_friends = current_user.get_suggested_friends()

    return [{'id': user.id,
             'username': user.username,
             'email': user.email,
             'country': get_user_country(user),
             'profile_picture': user.get_profile_picture_url()
             } for user in non_friends]


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user


def get_pending_requests():
    requests = current_user.get_pending_friend_requests()

    pending_requests = []
    for friend_request in requests:
        sender = get_user_by_id(friend_request.sender_id)

        pending_requests.append({
            'sender_username': sender.username,
            'sender_email': sender.email,
            'profile_picture': sender.get_profile_picture_url(),
            'country': get_user_country(sender)
        })

    return {
        'message': f'Pending requests for {current_user.username}',
        'pending_requests': [
            request for request in pending_requests
        ]
    }
