from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from social_app.friends import friends_bp
from social_app.friends.utils import get_non_friends_data, get_friends_data, get_user_by_username, \
    get_pending_requests


@friends_bp.get('/suggested_friends')
@jwt_required()
def get_suggested_friends():
    non_friends_data = get_non_friends_data()
    return jsonify({'suggested_friends': non_friends_data}), HTTPStatus.OK


@friends_bp.get('/friends')
@jwt_required()
def get_all_friends():
    friends_data = get_friends_data()
    return jsonify({'friends': friends_data}), HTTPStatus.OK


@friends_bp.post('/send_friend_request/<username>')
@jwt_required()
def send_friend_request(username):
    receiver = get_user_by_username(username)

    if not receiver:
        return jsonify({'message': 'Invalid receiver ID or cannot send friend request.'}), HTTPStatus.BAD_REQUEST

    current_user.send_friend_request(receiver)
    return jsonify({'message': 'Friend request sent successfully.'}), HTTPStatus.OK


@friends_bp.post('/accept_friend_request/<username>')
@jwt_required()
def accept_friend_request(username):
    sender = get_user_by_username(username)

    if not sender:
        return jsonify({'message': 'Invalid sender ID.'}), HTTPStatus.BAD_REQUEST

    current_user.accept_friend_request(sender)
    return jsonify({'message': 'Friend request accepted successfully.'}), HTTPStatus.OK


@friends_bp.post('/decline_friend_request/<username>')
@jwt_required()
def decline_friend_request(username):
    sender = get_user_by_username(username)

    if not sender:
        return jsonify({'message': 'Invalid sender ID.'}), HTTPStatus.BAD_REQUEST

    current_user.decline_friend_request(sender)
    return jsonify({'message': 'Friend request declined successfully.'}), HTTPStatus.OK


@friends_bp.get('/pending_friend_requests')
@jwt_required()
def get_pending_friend_requests():
    if not current_user:
        return jsonify({'message': 'User not found.'}), HTTPStatus.NOT_FOUND

    pending_requests = get_pending_requests()
    return jsonify(pending_requests), HTTPStatus.OK


@friends_bp.delete('/remove_friend/<username>')
@jwt_required()
def remove_friend(username):
    friend = get_user_by_username(username)

    if not friend:
        return jsonify({'message': 'Friend not found.'}), HTTPStatus.BAD_REQUEST

    current_user.remove_friend(friend)
    return jsonify({'message': 'Friend removed successfully.'}), HTTPStatus.OK
