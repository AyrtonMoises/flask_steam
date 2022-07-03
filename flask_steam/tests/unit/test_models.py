from flask_steam.blueprints.favorite.models import Game 



def test_create_game():
    """ Test create game """
    game = Game(
        steam_id=1382330,
        name='Persona® 5 Strikers (1382330)',
        logo_url='https://cdn.akamai.steamstatic.com/steam/apps/1382330/header.jpg'
    )

    assert game.steam_id == 1382330
    assert game.name == 'Persona® 5 Strikers (1382330)'
    assert game.logo_url == 'https://cdn.akamai.steamstatic.com/steam/apps/1382330/header.jpg'