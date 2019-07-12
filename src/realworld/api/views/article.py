# FIXME Handle User Not Found - 404 errors

from flask import request, Blueprint, jsonify

from realworld.application_services.command.create_article_command import CreateArticleCommand
from realworld.application_services.article_service import ArticleService

article_api = Blueprint('article_api', __name__)


@article_api.route('/api/articles/', methods=['POST'])
def create_article():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    if not auth_token:
        return '', 401

    data = request.json

    command = CreateArticleCommand(
        token=auth_token,
        title=data['article']['title'],
        description=data['article']['description'],
        body=data['article']['body'],
        tag_list=data['article']['tag_list']
    )

    article_resource = ArticleService.create_article(command)

    return jsonify(article_resource.to_dict()), 201
