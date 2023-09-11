from social_app.extensions import db


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)


# association table to make many-to-many relationship of a user with itself.
friends = db.Table('friends',
                   db.Column('user_id', db.Integer, db.ForeignKey(
                       'user.id')),
                   db.Column('friend_id', db.Integer, db.ForeignKey(
                       'user.id'))
                   )
