from datetime import datetime

from protean.core.field.basic import Identifier, Method, String

from realworld.domain import domain
from realworld.model.user import User


@domain.serializer(aggregate_cls=User)
class UserRepresentation:
    id = Identifier()
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    bio = String(max_length=1024)
    token = Method('token_only_if_active')

    def token_only_if_active(self, user):
        if user.token_valid_until and user.token_valid_until > datetime.now():
            return user.token
        else:
            return None
