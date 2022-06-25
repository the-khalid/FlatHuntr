from pickle import TRUE
from flask_googlemaps import GoogleMaps, Map
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

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

    # def __init__(self, id, email, username, password, number):
    #     self.id = id
    #     self.email = email
    #     self.username = username
    #     self.password = password
    #     self.number = number

class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default = func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def create_database(app):
    db.create_all(app=app)
    print("database created!")

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyA_RuK73hUDDWAxIOQt7IhvPbwkTmZ2wrU"
GoogleMaps(app)
app.config['SECRET_KEY']="helloworld"
#app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ckdjqmouhwgodo:4eaba8adfd322cb7f409611c08c0dd1ef2083b1656c69890c62771a33742746a@ec2-34-231-221-151.compute-1.amazonaws.com:5432/d21t5figogk86n'
app.debug=False
db.init_app(app)

from views import views
from auth import auth

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

create_database(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))