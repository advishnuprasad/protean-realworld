from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class UserRegistrationCommand:
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    password = String(required=True, max_length=255)
