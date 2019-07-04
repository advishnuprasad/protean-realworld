from flask import request, Blueprint, jsonify

from realworld.application_services.command.user_registration_command import UserRegistrationCommand
from realworld.application_services.user_registration_service import UserRegistrationService

user_api = Blueprint('user_api', __name__)


@user_api.route('/api/user/', methods=['POST'])
def register_user():
    data = request.json

    command = UserRegistrationCommand(
        email=data['user']['email'],
        username=data['user']['username'],
        password=data['user']['password']
    )

    user_resource = UserRegistrationService.register_user(command)

    return jsonify(user_resource.to_dict()), 201
