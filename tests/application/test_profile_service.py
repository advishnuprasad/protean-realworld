import pytest

from realworld.application_services.command.fetch_profile_command import FetchProfileCommand
from realworld.application_services.command.follow_profile_command import FollowProfileCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.profile_service import ProfileService
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.model.user import User


class TestProfileService:
    @pytest.fixture
    def persisted_users(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user1 = user_dao.create(email='john.doe@gmail.com', username='john.doe', password='secret1')
        user2 = user_dao.create(email='jane.doe@gmail.com', username='jane.doe', password='secret2')

        return [user1, user2]

    def test_successful_profile_fetch(self, persisted_users):
        user1 = persisted_users[0]
        user2 = persisted_users[1]
        auth_command = UserAuthenticationCommand(email=user1.email, password=user1.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        profile_command = FetchProfileCommand(token=authenticated_user['token'], username=user2.username)
        profile_resource = ProfileService.fetch_profile(profile_command)

        assert profile_resource is not None
        assert profile_resource['username'] == user2.username
        assert profile_resource['following'] is False

    def test_successful_profile_follow(self, persisted_users):
        user1 = persisted_users[0]
        user2 = persisted_users[1]

        auth_command = UserAuthenticationCommand(email=user1.email, password=user1.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        profile_command = FollowProfileCommand(token=authenticated_user['token'], username=user2.username)
        profile_resource = ProfileService.follow_profile(profile_command)

        assert profile_resource is not None
        assert profile_resource['username'] == user2.username
        assert profile_resource['following'] is True

    def test_successful_profile_unfollow(self, persisted_users):
        user1 = persisted_users[0]
        user2 = persisted_users[1]

        auth_command = UserAuthenticationCommand(email=user1.email, password=user1.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        profile_command = FollowProfileCommand(token=authenticated_user['token'], username=user2.username)
        profile_resource = ProfileService.follow_profile(profile_command)

        assert profile_resource['username'] == user2.username
        assert profile_resource['following'] is True

        # Now unfollow profile
        profile_command = FollowProfileCommand(token=authenticated_user['token'], username=user2.username)
        profile_resource = ProfileService.unfollow_profile(profile_command)

        assert profile_resource['username'] == user2.username
        assert profile_resource['following'] is False
