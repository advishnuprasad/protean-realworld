from protean.globals import current_domain

from realworld.application_services.command.fetch_profile_command import FetchProfileCommand
from realworld.application_services.command.follow_profile_command import FollowProfileCommand
from realworld.application_services.representation.profile_representation import ProfileRepresentation
from realworld.domain import domain
from realworld.model.user import User


@domain.application_service
class ProfileService:
    @classmethod
    def fetch_profile(cls, command: FetchProfileCommand):
        user_repo = current_domain.repository_for(User)
        logged_in_user = user_repo.get_by_token(command.token)

        if logged_in_user is not None:
            profile_user = user_repo.get_by_username(command.username)
            if profile_user is not None:
                profile_resource = ProfileRepresentation.for_user(logged_in_user, profile_user)
                return profile_resource

        return None

    @classmethod
    def follow_profile(cls, command: FollowProfileCommand):
        user_repo = current_domain.repository_for(User)
        logged_in_user = user_repo.get_by_token(command.token)

        if logged_in_user is not None:
            user_to_follow = user_repo.get_by_username(command.username)

            logged_in_user.follow(user_to_follow)
            user_repo.add(logged_in_user)

            fetch_command = FetchProfileCommand(token=command.token, username=user_to_follow.username)
            return cls.fetch_profile(fetch_command)

        return None

    @classmethod
    def unfollow_profile(cls, command: FollowProfileCommand):
        user_repo = current_domain.repository_for(User)
        logged_in_user = user_repo.get_by_token(command.token)

        if logged_in_user is not None:
            user_to_unfollow = user_repo.get_by_username(command.username)

            logged_in_user.unfollow(user_to_unfollow)
            user_repo.add(logged_in_user)

            fetch_command = FetchProfileCommand(token=command.token, username=user_to_unfollow.username)
            return cls.fetch_profile(fetch_command)

        return None
