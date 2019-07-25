from flask import Blueprint, jsonify

from realworld.application_services.tag_service import TagService

tag_api = Blueprint('tag_api', __name__)


@tag_api.route('/api/tags', methods=['GET'])
def fetch_tags():
    tags_resource = TagService.get_tags()

    return jsonify(tags_resource), 200
