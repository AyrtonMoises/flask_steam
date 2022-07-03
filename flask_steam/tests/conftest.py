import pytest

from flask_steam.app import create_app, minimal_app
from flask_steam.ext.database import db
from flask_steam.blueprints.favorite.models import Game
from flask_steam.blueprints.favorite.doa import save_game


@pytest.fixture(scope="session")
def min_app():
    app = minimal_app(FORCE_ENV_FOR_DYNACONF="testing")
    return app


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        db.create_all(app=app)
        yield app
        db.drop_all(app=app)


@pytest.fixture(scope="session")
def games(app):
    with app.app_context():
        data = [
            Game(name="Soul Hackers 2", steam_id=1777620, logo_url='https://cdn.akamai.steamstatic.com/steam/apps/1777620/header.jpg'),
            Game(name="Persona 4", steam_id=1113000, logo_url='https://cdn.akamai.steamstatic.com/steam/apps/1113000/header.jpg'),
            Game(name="God of War", steam_id=1593500, logo_url='https://cdn.akamai.steamstatic.com/steam/apps/1593500/header.jpg'),
        ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Game.query.all()
