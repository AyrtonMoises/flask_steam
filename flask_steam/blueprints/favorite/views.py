import json, locale

from flask import render_template, jsonify, url_for, redirect, request, flash
import requests

from flask_steam.ext.cache import cache
from flask_steam.blueprints.favorite.doa import delete_game, save_game, all_games, get_game


LINK_GAME_DETAILS = 'https://store.steampowered.com/api/appdetails?appids='

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')


def conversor_moeda(valor):
    moeda_convertida = requests.get('https://economia.awesomeapi.com.br/ARS-BRL/')
    moeda_convertida = json.loads(moeda_convertida.content)[0]['high']
    return locale.currency(
        float(moeda_convertida) * float(format(valor / 100, '.02f')), 
        grouping=True
    )

def busca_dados_steam(game_id):
    game_id_str = str(game_id)
    link = LINK_GAME_DETAILS + game_id

    # Busca dados do jogo no Brasil
    retorno = requests.get(link + '&cc=br&l=pt')
    json_retorno = json.loads(retorno.content)

    if json_retorno[game_id_str]['success'] == True:

        data_game = json_retorno[game_id_str]['data']
        preco_detalhes_br = data_game.get('price_overview', 0)

        # Busca dados na Argentina para buscar valor
        retorno_arg = requests.get(link + '&cc=ar')
        json_retorno_arg = json.loads(retorno_arg.content)

        if json_retorno_arg[game_id_str]['success'] == True:
            preco_detalhes_arg = json_retorno_arg[game_id_str]['data'].get('price_overview', 0)
        else:
            preco_detalhes_arg = 0

        # Converter moeda ARG para BRL
        if preco_detalhes_arg:
            moeda_hoje = conversor_moeda(preco_detalhes_arg['final'])
        else:
            moeda_hoje = 0

        return {
            'data_game': data_game,
            'preco_detalhes_br': preco_detalhes_br,
            'preco_detalhes_arg': preco_detalhes_arg,
            'moeda_hoje': moeda_hoje
        }

    else:
        return None


def index():
    """ Página principal """
    list_favorites = all_games()
    return render_template('index.html', list_favorites=list_favorites)

def game(game_id):
    """ Exibe detalhes do jogo """
    dados_steam = busca_dados_steam(game_id)

    if dados_steam:
        # Verifica se game esta salvo como favorito
        favorite = get_game(game_id)
        steam_id = favorite.steam_id if favorite else 0

        dados = {
            'id_game': game_id,
            'id_favorite': steam_id,
            'nome': dados_steam['data_game']['name'],
            'preco_detalhes': dados_steam['preco_detalhes_br'],
            'preco_detalhes_arg': dados_steam['preco_detalhes_arg'],
            'logo': dados_steam['data_game']['header_image'],
            'moeda_hoje': dados_steam['moeda_hoje']
        }
        return render_template('game_details.html', dados=dados)
    else:
        return render_template('404.html', title = '404'), 404
    

def save_favorite():
    """ Salva o jogo como favorito"""
    save_game(request.form)
    flash('Salvo com sucesso!')
    return redirect(url_for('favorite.index'))

def delete_favorite():
    """ Deleta favorito """
    delete_game(request.form['steam_id'])
    flash('Removido com sucesso!')
    return redirect(url_for('favorite.index'))


def search_values():
    """ Busca valores atualizados dos games favoritados """
    all_favorites = all_games()
    games_list = []

    for favorite in all_favorites:
        steam_id_string = str(favorite.steam_id)
        game_dict = {}

        dados_steam = busca_dados_steam(steam_id_string)

        if dados_steam:
            game_dict['id'] = steam_id_string
            game_dict['brl'] =  dados_steam['preco_detalhes_br']['final_formatted']
            game_dict['arg'] =  dados_steam['preco_detalhes_arg']['final_formatted']

            game_dict['conversao'] = conversor_moeda(dados_steam['preco_detalhes_arg']['final'])
            games_list.append(game_dict)

    
    return jsonify(games_list)



@cache.cached(timeout=86400, key_prefix="steam_list")
def steam_list():

    """ Lista jogos da steam """
    retorno = requests.get(
        'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    )
    json_retorno = json.loads(retorno.content)
    data_game = json_retorno['applist']['apps']

    return jsonify(data_game)