from protean.core.field.basic import Identifier, String

from realworld.domain import domain
from realworld.model.user import User


@domain.data_transfer_object
class UserRepresentation:
    id = Identifier()
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    bio = String(max_length=1024)

    @classmethod
    def from_user(cls, user: User):
        return UserRepresentation(
            id=user.id,
            email=user.email,
            username=user.username,
            bio=user.bio
        )
