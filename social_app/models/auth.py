from datetime import datetime
from flask import url_for

from social_app.extensions import db, bcrypt
from social_app.models.friends import FriendRequest, friends
from social_app.exceptions import FriendOperationException, NotAllowedException


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.String(500), default="")
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    has_profile_picture = db.Column(db.Boolean, default=False, nullable=False)
    games_played = db.Column(db.Integer, default=0)
    games_won = db.Column(db.Integer, default=0)
    friends = db.relationship('User', secondary=friends,
                              primaryjoin='User.id == friends.c.user_id',
                              secondaryjoin='User.id == friends.c.friend_id',
                              backref=db.backref('friend_of', lazy='dynamic'))

    country_code = db.Column(db.String(10), db.ForeignKey('country.code'), nullable=True)

    country = db.relationship('Country', back_populates='users')

    messages = db.relationship('Message', backref='user', lazy=True)

    def is_valid_user(self, given_password):
        return bcrypt.check_password_hash(self.password, given_password)

    def get_profile_picture_url(self):
        if not self.has_profile_picture:
            return ""
        filename = f'{self.username}.jpg'
        return url_for('static', filename='/uploads/' + filename, _external=True)

    def add_friend(self, friend):
        if not self.is_friend(friend):
            self.friends.append(friend)
            db.session.commit()
        else:
            raise FriendOperationException('You already have them as friend')

    def remove_friend(self, friend):

        if friend in self.friends:
            self.friends.remove(friend)
            db.session.commit()
        elif self in friend.friends:
            friend.friends.remove(self)
            db.session.commit()
        else:
            raise FriendOperationException('No friend found to remove with id')

    def get_friends(self):
        friends_list = list(self.friends) + list(self.friend_of)
        unique_friends = list(set(friends_list))

        return unique_friends

    def get_suggested_friends(self):
        all_users = User.query.filter(User.id != self.id).all()

        non_friends = [
            user for user in all_users
            if user not in self.friends and user not in self.friend_of
        ]

        return non_friends

    def send_friend_request(self, receiver):
        if self.is_request_valid(receiver):
            friend_request = FriendRequest(sender_id=self.id, receiver_id=receiver.id)
            db.session.add(friend_request)
            db.session.commit()
        else:
            raise FriendOperationException('Request already sent')

    def accept_friend_request(self, sender):
        friend_request = FriendRequest.query.filter_by(
            sender_id=sender.id, receiver_id=self.id).first()

        if friend_request and friend_request.receiver_id == self.id:
            self.add_friend(sender)
            db.session.delete(friend_request)
            db.session.commit()
        else:
            raise NotAllowedException('You are not authorized to perform this action')

    def decline_friend_request(self, sender):
        friend_request = FriendRequest.query.filter_by(
            sender_id=sender.id, receiver_id=self.id).first()

        if friend_request and friend_request.receiver_id == self.id:
            db.session.delete(friend_request)
            db.session.commit()
        else:
            raise FriendOperationException('You dont have a pending request with this id')

    def get_pending_friend_requests(self):
        friend_requests = FriendRequest.query.filter_by(receiver_id=self.id).all()

        return friend_requests

    def is_request_valid(self, receiver):
        is_valid = False
        if receiver != self and receiver not in self.friends:
            friend_request = FriendRequest.query.filter_by(
                sender_id=self.id, receiver_id=receiver.id
            ).first()
            is_valid = False if friend_request else True

        return is_valid

    def is_friend(self, other_user):
        return other_user in self.friends or self in other_user.friends
