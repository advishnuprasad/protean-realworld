from flask import request, Blueprint, jsonify

from realworld.application_services.command.fetch_profile_command import FetchProfileCommand
from realworld.application_services.command.follow_profile_command import FollowProfileCommand
from realworld.application_services.profile_service import ProfileService

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/api/profiles/<username>', methods=['GET'])
def fetch_profile(username):
    if not username:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    command = FetchProfileCommand(
        token=auth_token,
        username=username,
    )

    profile_resource = ProfileService.fetch_profile(command)

    return jsonify(profile_resource.to_dict()), 200


@profile_api.route('/api/profiles/<username>/follow', methods=['POST'])
def follow_profile(username):
    if not username:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    command = FollowProfileCommand(
        token=auth_token,
        username=username,
    )

    profile_resource = ProfileService.follow_profile(command)

    return jsonify(profile_resource.to_dict()), 200


@profile_api.route('/api/profiles/<username>/follow', methods=['DELETE'])
def unfollow_profile(username):
    if not username:
        return '', 400

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    command = FollowProfileCommand(
        token=auth_token,
        username=username,
    )

    profile_resource = ProfileService.unfollow_profile(command)

    return jsonify(profile_resource.to_dict()), 200
