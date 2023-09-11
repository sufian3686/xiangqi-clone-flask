from marshmallow import Schema, fields


class RegistrationSchema(Schema):
    username = fields.String(required=True)
    country_code = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
