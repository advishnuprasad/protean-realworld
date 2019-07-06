from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class UserUpdateCommand:
    token = String(required=True, max_length=1024)
    email = String(max_length=250)
    username = String(max_length=50)
    password = String(max_length=255)
    bio = String(max_length=1024)
    image = String(max_length=1024)
