from protean.core.field.basic import Boolean, String

from realworld.domain import domain
from realworld.model.user import User


@domain.data_transfer_object
class ProfileRepresentation:
    username = String(required=True, max_length=50)
    bio = String(max_length=1024)
    image = String(max_length=1024)
    following = Boolean()

    @classmethod
    def for_user(cls, user: User, profile_user: User):
        following = profile_user in [item.following for item in user.follows]

        return ProfileRepresentation(
            username=profile_user.username,
            bio=profile_user.bio,
            image=profile_user.image,
            following=following
        )
