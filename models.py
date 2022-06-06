from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    username  = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    number = db.Column(db.String(10))
    date_created = db.Column(db.DateTime(timezone=True), default = func.now())
    locations = db.relationship('Location', backref='user', passive_deletes = True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default = func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)