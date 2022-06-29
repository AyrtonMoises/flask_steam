
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv('.env')


app = Flask(__name__)

config = {
    "DEBUG": True,          
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app.config.from_mapping(config)
app.config.from_pyfile('config.py')

cache = Cache(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *




