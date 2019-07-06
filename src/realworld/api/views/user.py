# FIXME Handle User Not Found - 404 errors

from flask import request, Blueprint, jsonify

from realworld.application_services.command.current_user_command import CurrentUserCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.command.user_registration_command import UserRegistrationCommand
from realworld.application_services.command.user_update_command import UserUpdateCommand
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.application_services.user_registration_service import UserRegistrationService
from realworld.application_services.user_service import UserService

user_api = Blueprint('user_api', __name__)


@user_api.route('/api/users/', methods=['POST'])
def register_user():
    data = request.json

    command = UserRegistrationCommand(
        email=data['user']['email'],
        username=data['user']['username'],
        password=data['user']['password']
    )

    user_resource = UserRegistrationService.register_user(command)

    return jsonify(user_resource.to_dict()), 201


@user_api.route('/api/users/login', methods=['POST'])
def authenticate_user():
    data = request.json

    command = UserAuthenticationCommand(
        email=data['user']['email'],
        password=data['user']['password']
    )

    user_resource = UserAuthenticationService.authenticate_user(command)

    if user_resource:
        return jsonify(user_resource.to_dict()), 200
    else:
        return '', 401


@user_api.route('/api/user', methods=['GET'])
def fetch_logged_in_user():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None

    if not auth_token:
        return '', 401

    command = CurrentUserCommand(token=auth_token)

    user_resource = UserService.fetch_logged_in_user(command)
    if user_resource:
        return jsonify(user_resource.to_dict()), 200
    else:
        return '', 401


@user_api.route('/api/user/', methods=['PUT'])
def update_user():
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
    if 'email' in data['user'] and data['user']['email']:
        kwargs['email'] = data['user']['email']
    if 'username' in data['user'] and data['user']['username']:
        kwargs['username'] = data['user']['username']
    if 'password' in data['user'] and data['user']['password']:
        kwargs['password'] = data['user']['password']
    if 'image' in data['user'] and data['user']['image']:
        kwargs['image'] = data['user']['image']
    if 'bio' in data['user'] and data['user']['bio']:
        kwargs['bio'] = data['user']['bio']
    command = UserUpdateCommand(**kwargs)

    user_resource = UserService.update_user(command)

    return jsonify(user_resource.to_dict()), 204
