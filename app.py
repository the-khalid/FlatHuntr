from pickle import TRUE
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
#DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']="helloworld"
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://gmvzxmttqaegof:f387fa9a8986eeef841f40bf318a8d592da110425173a3e6b550390af5a61990@ec2-54-147-33-38.compute-1.amazonaws.com:5432/dccuihstebq90m'
    db.init_app(app)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from models import User, Location

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    #if not path.exists(DB_NAME):
    db.create_all(app=app)
     #   print("database created!")

if(__name__ == '__main__'):
    app = create_app()
    app.run(debug=TRUE)