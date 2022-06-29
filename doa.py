from app import db
from models import Game


def get_game(steam_id):
    game = Game.query.filter_by(steam_id=steam_id).first()
    return game

def all_games():
    games = Game.query.all()
    return games

def save_game(dados):
    game = Game(
        steam_id=dados['steam_id'],
        name=dados['name'],
        logo_url=dados['logo_url']
    )
    db.session.add(game)
    db.session.commit()

def delete_game(steam_id):
    game = Game.query.filter_by(steam_id=steam_id).first()
    db.session.delete(game)
    db.session.commit()


    
