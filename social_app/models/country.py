from social_app.extensions import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    users = db.relationship('User', back_populates='country')
