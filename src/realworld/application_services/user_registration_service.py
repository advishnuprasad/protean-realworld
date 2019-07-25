from protean.globals import current_domain

from realworld.application_services.command.user_registration_command import UserRegistrationCommand
from realworld.application_services.representation.user_representation import UserRepresentation
from realworld.infrastructure.db.user_repository import UserRepository  # noqa: F401  # FIXME No need to import
from realworld.model.user import User, UserRegistrationDTO
from realworld.domain import domain


@domain.application_service(aggregate_cls=User)
class UserRegistrationService:
    @classmethod
    def register_user(cls, command: UserRegistrationCommand):
        # Convert a Command Object into a DTO, to pass into the domain
        user_dto = UserRegistrationDTO(
            email=command.email,
            username=command.username,
            password=command.password
        )

        # Call a factory method to construct a User object
        user = User.register(user_dto)

        # Persist the new User object
        user_repo = current_domain.repository_for(User)
        user_repo.add(user)

        # Convert the persisted user object into a resource
        #   to be passed onto the callee
        user_resource = UserRepresentation().dump(user)
        return user_resource
