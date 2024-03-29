# FIXME Handle User Not Found - 404 errors
# FIXME Handle resource not returned errors - 404 errors

from flask import request, Blueprint, jsonify

from realworld.application_services.command.create_article_command import CreateArticleCommand
from realworld.application_services.command.delete_article_command import DeleteArticleCommand
from realworld.application_services.command.get_article_command import GetArticleCommand
from realworld.application_services.command.list_articles_command import ListArticlesCommand
from realworld.application_services.command.update_article_command import UpdateArticleCommand
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

    return jsonify(article_resource), 201


@article_api.route('/api/articles/<slug>', methods=['GET'])
def fetch_article(slug):
    if not slug:
        return '', 400

    command = GetArticleCommand(slug=slug)
    article_resource = ArticleService.get_article(command)

    return jsonify(article_resource), 200


@article_api.route('/api/articles', methods=['GET'])
def list_articles():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    tag = request.args.get('tag')
    author = request.args.get('author')
    favorited = request.args.get('favorited')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    command = ListArticlesCommand(
        token=auth_token, tag=tag, author=author,
        favorited=favorited, limit=limit, offset=offset)
    article_resources = ArticleService.list_articles(command)

    return jsonify(article_resources), 200


@article_api.route('/api/articles/<slug>', methods=['PUT'])
def update_article(slug):
    if not slug:
        return '', 400

    data = request.json

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    if not auth_token:
        return '', 401

    kwargs = {}
    kwargs['token'] = auth_token
    kwargs['slug'] = slug
    if 'title' in data['article'] and data['article']['title']:
        kwargs['title'] = data['article']['title']
    if 'description' in data['article'] and data['article']['description']:
        kwargs['description'] = data['article']['description']
    if 'body' in data['article'] and data['article']['body']:
        kwargs['body'] = data['article']['body']
    command = UpdateArticleCommand(**kwargs)

    article_resource = ArticleService.update_article(command)

    return jsonify(article_resource), 204


@article_api.route('/api/articles/<slug>', methods=['DELETE'])
def delete_article(slug):
    if not slug:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    if not auth_token:
        return '', 401

    kwargs = {'token': auth_token, 'slug': slug}
    command = DeleteArticleCommand(**kwargs)

    ArticleService.delete_article(command)

    return '', 204
