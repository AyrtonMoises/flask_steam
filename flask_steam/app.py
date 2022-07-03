from flask import Flask
from flask_steam.ext import configuration
from dotenv import load_dotenv


load_dotenv()

def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app

def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app
