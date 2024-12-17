from flask import Flask
from config import config
from flask_cors import *
import os
import datetime
import redis
from flask_httpauth import  HTTPTokenAuth
app = Flask(__name__)

auth = HTTPTokenAuth(scheme='Bearer')
CORS(app, supports_credentials=True)
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)

def create_app(config_name):

    # create the app
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = "abcdefg"
    config[config_name].init_app(app)
    from .api import api as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

