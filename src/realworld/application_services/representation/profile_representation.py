from protean.core.field.basic import Boolean, String

from realworld.domain import domain
from realworld.model.user import User


@domain.serializer(aggregate_cls=User)
class ProfileRepresentation:
    username = String(required=True, max_length=50)
    bio = String(max_length=1024)
    image = String(max_length=1024)
    following = Boolean()
