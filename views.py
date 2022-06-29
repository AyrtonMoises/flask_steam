import json

from flask import render_template, jsonify, url_for, redirect, request, flash
import requests

from app import app, cache
from doa import delete_game, save_game, all_games, get_game


def conversor_moeda(valor):
    moeda_convertida = requests.get('https://economia.awesomeapi.com.br/ARS-BRL/')
    moeda_convertida = json.loads(moeda_convertida.content)[0]['high']
    return round(
                float(moeda_convertida) * float(format(valor / 100, '.02f')
            ),  2)


@app.route('/')
def index():
    """ Página principal """
    list_favorites = all_games()
    return render_template('index.html', list_favorites=list_favorites)

@app.route("/game/<int:game_id>")
def game(game_id):
    """ Exibe detalhes do jogo """
    link = 'https://store.steampowered.com/api/appdetails?appids={}'\
        .format(game_id)

    # Busca dados do jogo no Brasil
    retorno = requests.get(link+'&cc=br&l=pt')
    json_retorno = json.loads(retorno.content)

    if json_retorno[f'{game_id}']['success'] == True:

        data_game = json_retorno[f'{game_id}']['data']
        preco_detalhes_br = data_game.get('price_overview', 0)

        # Busca dados na Argentina para buscar valor
        retorno_arg = requests.get(link + '&cc=ar')
        json_retorno_arg = json.loads(retorno_arg.content)

        if json_retorno_arg[f'{game_id}']['success'] == True:
            preco_detalhes_arg = json_retorno_arg[f'{game_id}']['data'].get('price_overview', 0)
        else:
            preco_detalhes_arg = 0

        # Converter moeda ARG para BRL
        if preco_detalhes_arg:
            moeda_hoje = conversor_moeda(preco_detalhes_arg['final'])
        else:
            moeda_hoje = 0

        # Verifica se game esta salvo como favorito
        favorite = get_game(game_id)
        steam_id = favorite.steam_id if favorite else 0

        dados = {
            'id_game': game_id,
            'id_favorite': steam_id,
            'nome': data_game['name'],
            'preco_detalhes': preco_detalhes_br,
            'preco_detalhes_arg': preco_detalhes_arg,
            'logo': data_game['header_image'],
            'moeda_hoje': moeda_hoje
        }
    else:
        return render_template('404.html', title = '404'), 404

  
    return render_template('game_details.html', dados=dados)

@app.route("/save_favorite/", methods=['POST',])
def save_favorite():
    """ Salva o jogo como favorito"""
    save_game(request.form)
    flash('Salvo com sucesso!')
    return redirect(url_for('index'))

@app.route("/delete_favorite/<int:id_favorite>")
def delete_favorite(id_favorite):
    """ Deleta favorito """
    delete_game(id_favorite)
    flash('Removido com sucesso!')
    return redirect(url_for('index'))


@app.route("/search_values/")
def search_values():
    """ Busca valores atualizados dos games favoritados """
    link = 'https://store.steampowered.com/api/appdetails?appids='
    all_favorites = all_games()

    games_list = []
    for favorite in all_favorites:
        game_dict = {}
        
        # Valor Brasil
        response = requests.get(link + f'{favorite.steam_id}&cc=br')
        content_json = json.loads(response.content)
        
        if content_json[str(favorite.steam_id)]['success'] == True:
            price_overview_br = content_json[str(favorite.steam_id)]['data'].get('price_overview', 0)

            game_dict['id'] = favorite.steam_id
            game_dict['brl'] = price_overview_br['final_formatted']

            # Valor Argentina
            response = requests.get(link + f'{favorite.steam_id}&cc=ar')
            content_json = json.loads(response.content)
            
            if content_json[str(favorite.steam_id)]['success'] == True:
                price_overview_arg = content_json[str(favorite.steam_id)]['data'].get('price_overview', 0)

                game_dict['arg'] = price_overview_arg['final_formatted']
                game_dict['conversao'] = conversor_moeda(price_overview_arg['final'])
            games_list.append(game_dict)

    return jsonify(games_list)

@app.route('/steam-list/')
@cache.cached(timeout=86400)
def steam_list():
    """ Lista jogos da steam """
    retorno = requests.get(
        'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    )
    json_retorno = json.loads(retorno.content)
    data_game = json_retorno['applist']['apps']

    return jsonify(data_game)
