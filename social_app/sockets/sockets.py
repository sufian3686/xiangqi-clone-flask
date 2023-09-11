import random
from flask_socketio import emit, join_room, leave_room, close_room

from social_app.models.auth import User
from social_app.extensions import db
from social_app.models.chat import Message
from social_app.extensions import socketio
from social_app.profile.utils import get_user_country

XIANGQI = '/xiangqi'
active_rooms = {}


@socketio.on('connect', namespace=XIANGQI)
def connect():
    join_room('announcements')


@socketio.on('disconnect', namespace=XIANGQI)
def disconnect():
    leave_room('announcements')


@socketio.on('chat.join', namespace=XIANGQI)
def chat_join():
    join_room("chat")
    messages = get_existing_messages()
    emit('existing_messages', {'messages': messages}, room='chat')


@socketio.on('chat.message', namespace=XIANGQI)
def send_message(data):
    message_text = data['text']
    username = data['username']
    user = User.query.filter_by(username=username).first()

    if user:
        message = Message(text=message_text, user=user)
        db.session.add(message)
        db.session.commit()

        emit('new_message', {
            'message': {
                'text': message.text,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'username': message.user.username,
                'country': get_user_country(message.user),
                'image': message.user.get_profile_picture_url()
            }
        }, to='chat')


@socketio.on('chat.leave', namespace=XIANGQI)
def chat_leave():
    leave_room("chat")


def get_existing_messages():
    existing_messages = Message.query.order_by(Message.timestamp).all()
    messages = [{
        'text': message.text,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'username': message.user.username,
        'country': get_user_country(message.user),
        'image': message.user.get_profile_picture_url()
    } for message in existing_messages]
    return messages


@socketio.on('game.create', namespace=XIANGQI)
def create_game(data):
    room_id = str(random.randint(1000, 9999))
    active_rooms[room_id] = {'players': [data['username']]}
    join_room(room_id)
    emit('game_created', {'room_id': room_id}, to=room_id, namespace='/xiangqi')
    emit('room_added', {'rooms': active_rooms}, to='announcements', namespace='/xiangqi')


@socketio.on('game.rooms', namespace=XIANGQI)
def get_rooms():
    emit('game_rooms', {'rooms': active_rooms}, namespace=XIANGQI)


@socketio.on('game.move', namespace=XIANGQI)
def piece_move(data):
    room_id = data['roomId']
    emit('piece_moved', {'move_details': data}, to=room_id, namespace='/xiangqi')


@socketio.on('game.quit', namespace=XIANGQI)
def quit_game(data):
    room_id = data['roomId']
    emit('game_abandoned', to=room_id, namespace='/xiangqi')

    close_room(room_id)
    if room_exists(room_id):
        del active_rooms[room_id]

    emit('room_removed', {'rooms': active_rooms}, to='announcements', namespace='/xiangqi')


@socketio.on('game.join', namespace=XIANGQI)
def join_game(data):
    room_id = data['room_id']
    username = data['username']

    if room_exists(room_id) and room_not_full(room_id):
        join_room_and_emit(room_id, username)

        if room_is_full(room_id):
            remove_room(room_id)
    else:
        emit_room_not_found()


def room_exists(room_id):
    return room_id in active_rooms


def room_not_full(room_id):
    return len(active_rooms[room_id]['players']) < 2


def join_room_and_emit(room_id, username):
    active_rooms[room_id]['players'].append(username)
    join_room(room_id)
    emit('game.room_joined', {'room_id': room_id, 'players': active_rooms[room_id]['players']}, to=room_id,
         namespace=XIANGQI)


def room_is_full(room_id):
    return len(active_rooms[room_id]['players']) == 2


def remove_room(room_id):
    del active_rooms[room_id]


def emit_room_not_found():
    emit('game.room_not_found', namespace=XIANGQI)
