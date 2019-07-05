from protean.globals import current_domain

from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.representation.user_representation import UserRepresentation
from realworld.infrastructure.user_repository import UserRepository  # noqa: F401  # FIXME No need to import
from realworld.model.user import User
from realworld.domain import domain


@domain.application_service
class UserAuthenticationService:
    @classmethod
    def authenticate_user(cls, command: UserAuthenticationCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_email(command.email)

        # Call a factory method to authenticate User with given password
        valid = user.authenticate(command.password)

        if valid:
            # Convert the persisted user object into a resource
            #   to be passed onto the callee
            user_resource = UserRepresentation.from_user(user)
            return user_resource

        return None
