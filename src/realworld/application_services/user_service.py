from protean.globals import current_domain

from realworld.application_services.command.current_user_command import CurrentUserCommand
from realworld.application_services.command.user_fetch_command import UserFetchCommand
from realworld.application_services.command.user_update_command import UserUpdateCommand
from realworld.application_services.representation.user_representation import UserRepresentation
from realworld.infrastructure.db.user_repository import UserRepository  # noqa: F401  # FIXME No need to import
from realworld.model.user import User
from realworld.domain import domain


@domain.application_service
class UserService:
    @classmethod
    def fetch_user(cls, command: UserFetchCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_username(command.username)

        if user is not None:
            # Convert the persisted user object into a resource
            #   to be passed onto the callee
            user_resource = UserRepresentation().dump(user)
            return user_resource

        return None

    @classmethod
    def fetch_logged_in_user(cls, command: CurrentUserCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            # Convert the persisted user object into a resource
            #   to be passed onto the callee
            user_resource = UserRepresentation().dump(user)
            return user_resource

        return None

    @classmethod
    def update_user(cls, command: UserUpdateCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            kwargs = command.to_dict()
            kwargs.pop('token', None)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            user.update(**kwargs)
            user_repo.add(user)

            user_resource = UserRepresentation().dump(user)
            return user_resource

        return None
