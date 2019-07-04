from protean.globals import current_domain

from realworld.application_services.command.user_registration_command import UserRegistrationCommand
from realworld.application_services.representation.user_representation import UserRepresentation
from realworld.infrastructure.user_repository import UserRepository  # noqa: F401  # FIXME No need to import
from realworld.model.user import User, UserRegistrationDTO
from realworld.domain import domain


@domain.application_service
class UserRegistrationService:
    @classmethod
    def register_user(cls, command: UserRegistrationCommand):
        user_dto = UserRegistrationDTO(
            email=command.email,
            username=command.username,
            password=command.password
        )
        user = User.register_user(user_dto)

        user_repo = current_domain.repository_for(User)
        user_repo.add(user)

        user_resource = UserRepresentation.from_user(user)

        return user_resource
