import pytest

from datetime import datetime, timedelta

from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.command.user_fetch_command import UserFetchCommand
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.application_services.user_service import UserService
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

    def test_presence_of_token_after_successful_authentication(self, persist_user):
        command = UserAuthenticationCommand(
            email='jake@jake.jake', password='nopass'
            )

        user_resource = UserAuthenticationService.authenticate_user(command)
        assert user_resource['token'] is not None

    def test_that_user_token_is_empty_if_authentication_was_more_than_a_day_ago(self, persist_user, test_domain):
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')

        user_resource = UserAuthenticationService.authenticate_user(command)
        assert user_resource['token'] is not None

        # Change valid_until timestamp manually to test scenario
        user_dao = test_domain.get_dao(User)
        persisted_user = user_dao.get(user_resource['id'])
        persisted_user.token_valid_until = datetime.now() - timedelta(days=2)
        user_dao.save(persisted_user)

        command = UserFetchCommand(username=user_resource['username'])
        user_resource = UserService.fetch_user(command)
        assert user_resource['token'] is None

    def test_unsuccessful_user_authentication(self, persist_user):
        command = UserAuthenticationCommand(
            email='jake@jake.jake', password='wrongpass'
            )

        user_resource = UserAuthenticationService.authenticate_user(command)
        assert user_resource is None
