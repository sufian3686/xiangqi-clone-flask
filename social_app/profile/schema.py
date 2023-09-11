from marshmallow import Schema, fields

from social_app.profile.utils import get_user_friends_data, get_user_created_date, get_user_country


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    bio = fields.String()
    games_played = fields.Integer()
    games_won = fields.Integer()
    profile_picture = fields.Method("get_image_url")

    friends = fields.Method("get_user_friends_data")
    created_on = fields.Method("get_user_created_date")

    country = fields.Method("get_country")

    def get_image_url(self, user):
        return user.get_profile_picture_url()

    def get_user_friends_data(self, user):
        return get_user_friends_data(user)

    def get_user_created_date(self, user):
        return get_user_created_date(user)

    def get_country(self, user):
        return get_user_country(user)
