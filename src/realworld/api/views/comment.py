from flask import request, Blueprint, jsonify

from realworld.application_services.command.add_comment_command import AddCommentCommand
from realworld.application_services.command.delete_comment_command import DeleteCommentCommand
from realworld.application_services.command.get_comment_command import GetAllCommentsCommand
from realworld.application_services.comment_service import CommentService

comment_api = Blueprint('comment_api', __name__)


@comment_api.route('/api/articles/<slug>/comments', methods=['GET'])
def fetch_comments(slug):
    if not slug:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    command = GetAllCommentsCommand(
        token=auth_token,
        slug=slug
    )

    comment_resource = CommentService.get_comments(command)

    return jsonify(comment_resource), 200


@comment_api.route('/api/articles/<slug>/comments', methods=['POST'])
def add_comment(slug):
    if not slug:
        return '', 400

    data = request.json

    # FIXME Provide a better way of doing these validations?
    if 'comment' not in data or 'body' not in data['comment']:
        return '', 400

    # FIXME Authentication could be a flask decorator
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    command = AddCommentCommand(
        token=auth_token,
        slug=slug,
        body=data['comment']['body']
    )

    comment_resource = CommentService.add_comment(command)

    return jsonify(comment_resource), 200


@comment_api.route('/api/articles/<slug>/comments/<identifier>', methods=['DELETE'])
def delete_comment(slug, identifier):
    if not slug or not identifier:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    command = DeleteCommentCommand(
        token=auth_token,
        slug=slug,
        comment_identifier=identifier
    )

    CommentService.delete_comment(command)

    return '', 204
