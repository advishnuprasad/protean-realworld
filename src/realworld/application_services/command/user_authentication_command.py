from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class UserAuthenticationCommand:
    email = String(required=True, max_length=250)
    password = String(required=True, max_length=255)
