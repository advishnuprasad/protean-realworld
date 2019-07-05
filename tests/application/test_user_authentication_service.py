import pytest

from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.model.user import User


class TestUserAuthenticationService:
    @pytest.fixture
    def persist_user(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user_dao.create(email='jake@jake.jake', username='jake', password='nopass')

    def test_successful_user_authentication(self, persist_user):
        command = UserAuthenticationCommand(
            email='jake@jake.jake', password='nopass'
            )

        user_resource = UserAuthenticationService.authenticate_user(command)
        assert user_resource is not None

    def test_unsuccessful_user_authentication(self, persist_user):
        command = UserAuthenticationCommand(
            email='jake@jake.jake', password='wrongpass'
            )

        user_resource = UserAuthenticationService.authenticate_user(command)
        assert user_resource is None
