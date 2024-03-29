from flask import Flask
from flask_steam.ext import configuration
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dynaconf import settings


load_dotenv()

def minimal_app(**config):
    sentry_sdk.init(
        dsn=settings('SENTRY_DSN'),
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0
    )

    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app

def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app
