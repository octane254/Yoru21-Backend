from flask import Flask
from .config import Config
from .db import db,migrate
from app.routes import users_bp
from .models import *
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt()
jwt=JWTManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    #initialize db
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app