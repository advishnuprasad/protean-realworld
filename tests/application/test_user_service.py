import pytest

from realworld.application_services.command.current_user_command import CurrentUserCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.command.user_fetch_command import UserFetchCommand
from realworld.application_services.command.user_update_command import UserUpdateCommand
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.application_services.user_service import UserService
from realworld.model.user import User


class TestUserService:
    # FIXME Implement failure test cases for User Not Found

    @pytest.fixture
    def persisted_user(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user = user_dao.create(email='jake@jake.jake', username='jake', password='nopass')

        return user

    def test_successful_user_fetch(self, persisted_user):
        command = UserFetchCommand(username=persisted_user.username)

        user_resource = UserService.fetch_user(command)
        assert user_resource is not None
        assert user_resource['email'] == 'jake@jake.jake'

    def test_unsuccessful_user_fetch(self, persisted_user):
        command = UserFetchCommand(username='foobar')

        user_resource = UserService.fetch_user(command)
        assert user_resource is None

    def test_fetching_current_logged_in_user_by_auth_token(self, persisted_user):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = CurrentUserCommand(token=authenticated_user['token'])
        logged_in_user = UserService.fetch_logged_in_user(command)
        assert authenticated_user == logged_in_user

    def test_updating_the_current_logged_in_user(self, persisted_user):
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = UserUpdateCommand(token=authenticated_user['token'], bio='I am the man!')
        updated_user = UserService.update_user(command)
        assert updated_user['bio'] == 'I am the man!'
