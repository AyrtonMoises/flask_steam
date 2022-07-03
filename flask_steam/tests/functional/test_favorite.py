from flask import request
from flask_steam.blueprints.favorite.doa import get_game
from flask_steam.blueprints.favorite.views import busca_dados_steam, conversor_moeda

def test_index_page(client, games):
    """ Teste pagina principal """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Favoritos" in response.data

    for game in games:
        assert bytes(str(game.steam_id), 'UTF-8') in response.data
        assert bytes(game.name, 'UTF-8') in response.data
        assert bytes(game.logo_url, 'UTF-8') in response.data

def test_save_favorite(client):
    """ Teste salvar game como favorito """
    data = {
        'steam_id': 1382330,
        'name': 'Persona® 5 Strikers (1382330)',
        'logo_url': 'https://cdn.akamai.steamstatic.com/steam/apps/1382330/header.jpg'
    }

    response = client.post('/save-favorite/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert request.path == '/'

    game_data = get_game(data['steam_id'])
    assert game_data.steam_id == data['steam_id']
    assert game_data.name == data['name']
    assert game_data.logo_url == data['logo_url']


def test_save_favorite_error(client):
    """ Teste salvar game com dados incorretos """
    data = {
        'steam_id': '123',
        'name': 'Nome do jogo',
        'logo_url': None
    }
    response = client.post('/save-favorite/', data=data, follow_redirects=True)
    assert response.status_code == 400


def test_delete_favorite(client):
    """ Teste deletar favorito """
    steam_id = 1777620 # Soul Hackers 2
    response = client.post('/delete-favorite/', data={'steam_id': steam_id}, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert request.path == '/'
    assert get_game(steam_id) == None

def test_game_page(client):
    """ Teste busca dados de jogo na steam """
    steam_id = '1382330' # Persona 5 Strikers
    response = client.get('/game/' + steam_id)
    assert response.status_code == 200
    dados_steam = busca_dados_steam(steam_id)

    assert bytes(dados_steam['data_game']['name'], 'UTF-8') in response.data
    assert bytes(dados_steam['preco_detalhes_br']['final_formatted'], 'UTF-8') in response.data
    assert bytes(dados_steam['preco_detalhes_arg']['final_formatted'], 'UTF-8') in response.data
    assert bytes(
        conversor_moeda(dados_steam['preco_detalhes_arg']['final']), 'UTF-8'
    ) in response.data
    assert bytes(dados_steam['data_game']['name'],'UTF-8') in response.data

def test_search_values_steam(client):
    """ Testa json que retorna valores da steam nos favoritos cadastrados """
    response = client.get("/search-values/")
    assert response.status_code == 200

    data = response.json

    assert len(data) == 3

    assert set(list(data[0].keys())) == set(['id', 'arg', 'brl','conversao'])