from flask import request, Blueprint, jsonify

from realworld.application_services.command.favorite_article_command import FavoriteArticleCommand
from realworld.application_services.command.unfavorite_article_command import UnfavoriteArticleCommand
from realworld.application_services.user_favoriting_service import UserFavoritingService

favorite_api = Blueprint('favorite_api', __name__)


@favorite_api.route('/api/articles/<slug>/favorite', methods=['POST'])
def favorite_article(slug):
    if not slug:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    favorite_command = FavoriteArticleCommand(token=auth_token, slug=slug)
    article_resource = UserFavoritingService.favorite_article(favorite_command)

    return jsonify(article_resource), 200


@favorite_api.route('/api/articles/<slug>/favorite', methods=['DELETE'])
def unfavorite_article(slug):
    if not slug:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    unfavorite_command = UnfavoriteArticleCommand(token=auth_token, slug=slug)
    article_resource = UserFavoritingService.unfavorite_article(unfavorite_command)

    return jsonify(article_resource), 200
