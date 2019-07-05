from flask import request, Blueprint, jsonify

from realworld.application_services.command.current_user_command import CurrentUserCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.command.user_registration_command import UserRegistrationCommand
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
