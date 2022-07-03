from flask import Blueprint

from .views import index, game, save_favorite, delete_favorite, search_values, steam_list


favorite_bp = Blueprint("favorite", __name__, template_folder="templates")

favorite_bp.add_url_rule("/", view_func=index)
favorite_bp.add_url_rule(
    "/game/<string:game_id>", view_func=game, endpoint="game"
)
favorite_bp.add_url_rule(
    "/save-favorite/", view_func=save_favorite, endpoint="save_favorite", methods=['POST',]
)
favorite_bp.add_url_rule(
    "/delete-favorite/", view_func=delete_favorite, endpoint="delete_favorite", 
    methods=['POST',]
)
favorite_bp.add_url_rule(
    "/search-values/", view_func=search_values, endpoint="search_values"
)
favorite_bp.add_url_rule(
    "/steam-list/", view_func=steam_list, endpoint="steam_list"
)


def init_app(app):
    app.register_blueprint(favorite_bp)